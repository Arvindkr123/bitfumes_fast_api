from fastapi import FastAPI

app = FastAPI();

@app.get("/")
def index():
    return {
        'data':'blog list'
    }
    
@app.get("/blog/{id}")
def about(id):
    return {
        'data':f'blog {id}'
    }

@app.get('/blog/{id}/comments')
def comments(id):
    return {
        'data':{
            '1','2'
        }
    }