from fastapi import FastAPI
from .database import engine
from . import models
from .routers import user, blog

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(blog.router)

