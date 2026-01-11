from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import engine, SessionLocal
from . import schemas, models
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['blogs'])
def getAllBlogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        return [];
    return blogs
    
@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=blog.title,
        body=blog.body,
        user_id=blog.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_200_OK, tags=['blogs'])
def destroy(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog)\
        .filter(models.Blog.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog deleted successfully"}

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
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
    


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def showBlog(id:int,response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with this id {id} is not available')
    return blog

@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser,tags=['users'])
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with this id {id} is not available');
    return user

@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get(
    "/users",
    response_model=List[schemas.ShowUser],
    status_code=status.HTTP_200_OK,
    tags=['users']
)
def showUsers(db: Session = Depends(get_db)):
    return db.query(models.User).all()



