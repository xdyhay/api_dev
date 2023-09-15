from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, like, auth

"""The Base class from models.py is imported and then used to create the tables in the database.
Comment out the following line to prevent the tables from being created.
Alembic will generate the SQL to create the tables"""
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(like.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {'message': 'Hello World'}