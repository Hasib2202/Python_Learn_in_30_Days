
from fastapi import FastAPI
from app.routes import auth

app = FastAPI(title="User Authentication API")

app.include_router(auth.router)
    