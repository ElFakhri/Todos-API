from typing import Annotated

from fastapi import HTTPException, status, Depends, Path, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import SessionLocal
import schemas
import todo_crud
import user_crud
import models
import security
import jwt
from jwt.exceptions import InvalidTokenError


router = APIRouter(prefix="/api")


# DEPENDENCIES


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User -------------------------------------------------------------------
oauth_scheme = OAuth2PasswordBearer(tokenUrl="api/login/")


@router.post("/register/")
def register(obj_in: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, obj_in=obj_in)


@router.post("/login/")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    obj_in = schemas.UserLogin(
        username=form_data.username, password=form_data.password
    )
    user = user_crud.login(db=db, obj_in=obj_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username or password is incorrect",
        )
    else:
        return {
            "access_token": security.create_token(username=user.username),
            "token_type": "Bearer",
        }


# Todo ---------------------------------------------------------------------


def get_current_user(
    token: Annotated[str, Depends(oauth_scheme)], db: Session = Depends(get_db)
):
    print(token)
    try:
        payload = jwt.decode(token, security.secret_key, algorithms=["HS256"])
        username = payload.get("sub")
    except InvalidTokenError:
        pass

    print(payload)
    user = user_crud.get_user_by_username(db=db, username=username)
    return user


def get_todo(
    id: int = Path(),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> models.Todo:
    todo = todo_crud.get_todo(db=db, id=id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo does not exist"
        )
    if user.email != todo.owner_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized",
        )
    return todo


@router.get("/todos/", response_model=list[schemas.Todo])
def get_todos(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return sorted(
        todo_crud.get_todos(db, user=current_user),
        key=lambda t: t.last_updated_date,
        reverse=True,
    )


@router.get("/todos/{id}", response_model=schemas.Todo)
def get_todo_by_id(todo: models.Todo = Depends(get_todo)):
    return todo


@router.post("/todos/")
def add_todo(
    todo_in: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    todo = todo_crud.create_todo(db=db, obj_in=todo_in, user=current_user)
    return todo


@router.delete("/todos/{id}")
def delete_todo(
    todo: models.Todo = Depends(get_todo), db: Session = Depends(get_db)
):
    todo_crud.delete_todo(db=db, db_obj=todo)
    return None


@router.put("/todos/{id}")
def update_todo(
    todo_in: schemas.TodoUpdate,
    todo: models.Todo = Depends(get_todo),
    db: Session = Depends(get_db),
):
    return todo_crud.update_todo(db=db, db_obj=todo, obj_in=todo_in)


@router.patch("/todos/{id}/is-done")
def toggle_completion(
    todo: models.Todo = Depends(get_todo), db: Session = Depends(get_db)
):
    return todo_crud.toggle_completion(db=db, db_obj=todo)
