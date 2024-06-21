from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import api
import pages

import models
from database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount("/img", StaticFiles(directory="static/img"), name="img")
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")

app.include_router(api.router, tags=["api"])
app.include_router(pages.router, tags=["pages"])
