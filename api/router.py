from fastapi import HTTPException, status, Depends, Path, APIRouter
from sqlalchemy.orm import Session

from database import SessionLocal
import schemas
import todo_crud
import user_crud
import models


router = APIRouter(prefix="/api")


# DEPENDENCIES


# Todo ---------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_todo(id: int = Path(), db: Session = Depends(get_db)) -> models.Todo:
    todo = todo_crud.get_todo(db=db, id=id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo does not exist"
        )
    return todo


@router.get("/todos/", response_model=list[schemas.Todo])
def get_todos(db: Session = Depends(get_db)):
    return sorted(
        todo_crud.get_todos(db), key=lambda t: t.last_updated_date, reverse=True
    )


@router.get("/todos/{id}", response_model=schemas.Todo)
def get_todo_by_id(todo: models.Todo = Depends(get_todo)):
    return todo


@router.post("/todos/")
def add_todo(todo_in: schemas.TodoCreate, db: Session = Depends(get_db)):
    todo = todo_crud.create_todo(db=db, obj_in=todo_in)
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


# User -------------------------------------------------------------------


@router.post("/register/")
def register(obj_in: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, obj_in=obj_in)


@router.post("/login/")
def login(obj_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = user_crud.login(db=db, obj_in=obj_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username or password is incorrect",
        )
    else:
        return user
