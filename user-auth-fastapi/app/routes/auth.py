
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserCreate, UserOut
from app.utils import create_access_token, verify_password, get_password_hash
from app.models import fake_users_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.email] = {"email": user.email, "password": hashed_password}
    return {"email": user.email}

@router.post("/login")
def login(user: UserCreate):
    db_user = fake_users_db.get(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
    