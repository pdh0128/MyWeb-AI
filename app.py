from fastapi import FastAPI
from fastapi.responses import JSONResponse
from search import vec_search, vec_store, vec_delete, vec_update
from pydantic import BaseModel
app = FastAPI()


class Text(BaseModel):
    Text : str

@app.post("/api/vecterSearch")
def search(text: Text):
    text = str(text)
    simi = vec_search(text)
    return JSONResponse({"serach" : simi})

class Post(BaseModel):
    PostId : int
    Title : str
    Content : str

@app.post("/api/vecterStore")
def store(post: Post):
    vec_store(post.PostId, post.Title, post.Content)
    return JSONResponse({"status": "ok"})

class PostId(BaseModel):
    PostId: int

@app.post("/api/vecterDelete")
def delete(PostId : PostId):
    vec_delete(PostId)
    return JSONResponse({"status": "ok"})

@app.post("/api/vecterUpdate")
def store(post: Post):
    vec_update(post.PostId, post.Title, post.Content)
    return JSONResponse({"status": "ok"})
