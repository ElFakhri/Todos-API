from sqlalchemy.orm import Session
import schemas
import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, obj_in: schemas.UserCreate):
    hashed_password = pwd_context.hash(obj_in.password)
    db_in = models.User(
        username=obj_in.username,
        email=obj_in.email,
        is_male=obj_in.is_male,
        hashed_password=hashed_password,
    )
    db.add(db_in)
    db.commit()
    db.refresh(db_in)

    return db_in


def login(db: Session, obj_in: schemas.UserLogin) -> models.User:
    user = (
        db.query(models.User)
        .filter(models.User.username == obj_in.username)
        .first()
    )
    if not user:
        return None
    if not pwd_context.verify(obj_in.password, user.hashed_password):
        return None

    return user


def get_user_by_username(db: Session, username: str):
    user = (
        db.query(models.User).filter(models.User.username == username).first()
    )

    return user
