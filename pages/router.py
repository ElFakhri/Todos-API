from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from api.router import get_todo
import schemas

router = APIRouter()

templates = Jinja2Templates("template")


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/todo/create")
def todo_create(request: Request):
    return templates.TemplateResponse(request=request, name="create.html")


@router.get("/todo/{id}")
def todo_detail(
    id: int, request: Request, todo: schemas.Todo = Depends(get_todo)
):
    return templates.TemplateResponse(
        request=request,
        name="detail.html",
        context={
            "title": todo.title,
            "description": todo.description,
            "id": todo.id,
        },
    )


@router.get("/todo/{id}/edit")
def todo_edit(
    id: int, request: Request, todo: schemas.Todo = Depends(get_todo)
):
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"title": todo.title, "description": todo.description},
    )


# USER LOGIN AND REGISTER


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")
