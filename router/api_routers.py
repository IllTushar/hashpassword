from fastapi import APIRouter, status, HTTPException, Depends
from engine.db_connection import engine, Base, SessionLocal
from model.model_file import UserRegisterRequest
from sqlalchemy.orm import Session
from table.register_table import Registration
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/user-registration", status_code=status.HTTP_201_CREATED)
def post_registration(request: UserRegisterRequest, db: Session = Depends(connect_db)):
    try:
        create_user = Registration(name=request.name, email=request.email, password=pwd_context.hash(request.password))
        db.add(create_user)
        db.commit()
        db.refresh(create_user)
        return create_user
    except Exception as e:
        # Log the error if you have a logging system in place
        print(f"Error: {e}")
        raise HTTPException(status_code=422, detail="Email already exists!")


def verify_user(email, password, db):
    data = db.query(Registration).filter(Registration.email == email).first()
    if not data:
        return False
    if not pwd_context.verify(password, data.password):
        return False
    return True


@router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(connect_db)):
    login_user = verify_user(form_data.username, form_data.password, db)
    if not login_user:
        return "Failed"
    return {"message": "Successful"}
