from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .. import database, schemas, models, hashing
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)
get_db = database.get_db

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def getAllBlogs(db: Session = Depends(get_db)):
    return blog.getAll(db)
    
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db);
    
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.delete(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db);

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def showBlog(id:int, db: Session = Depends(get_db)):
    return blog.getBlogById(id, db);
