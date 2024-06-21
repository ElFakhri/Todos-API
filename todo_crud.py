from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas


def get_todos(db: Session, user: models.User):  # get a list of every todos
    return (
        db.query(models.Todo)
        .filter(models.Todo.owner_email == user.email)
        .all()
    )


def get_todo(db: Session, id: int):  # get a todo
    return db.query(models.Todo).filter(models.Todo.id == id).first()


def create_todo(db: Session, obj_in: schemas.TodoCreate, user: models.User):
    db_in = models.Todo(
        title=obj_in.title,
        description=obj_in.description,
        created_date=datetime.now(),
        last_updated_date=datetime.now(),
        is_done=False,
        owner_email=user.email,
    )

    db.add(db_in)
    db.commit()
    db.refresh(db_in)
    return db_in


def delete_todo(db: Session, db_obj: models.Todo):
    db.delete(db_obj)
    db.commit()


def toggle_completion(db: Session, db_obj: models.Todo):
    db_obj.is_done = not db_obj.is_done
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_todo(db: Session, db_obj: models.Todo, obj_in: schemas.TodoUpdate):
    db_obj.title = obj_in.title
    db_obj.description = obj_in.description
    db_obj.last_updated_date = datetime.now()
    db.commit()
    db.refresh(db_obj)
    return db_obj
