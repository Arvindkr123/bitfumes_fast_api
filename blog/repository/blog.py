from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from .. import models, schemas



def getAll(db: Session):
    blogs = db.query(models.Blog).all()
    if not blogs:
        return [];
    return blogs

def create(request:schemas.BlogCreate, db:Session):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=request.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id:int, db:Session):
    db.query(models.Blog)\
        .filter(models.Blog.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog deleted successfully"}

def update(id:int, request:schemas.BlogCreate, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return {"detail": "Blog updated successfully"}

def getBlogById(id:int, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} is not available')
    return blog
