from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, schemas, models, hashing
from sqlalchemy.orm import Session
from typing import List
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
);

get_db = database.get_db

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id:int, db:Session=Depends(get_db)):
    return user.getUserById(id, db);

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get(
    "/",
    response_model=List[schemas.ShowUser],
    status_code=status.HTTP_200_OK
)
def showUsers(db: Session = Depends(get_db)):
    return user.getAll(db)


