from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
            "message" : "Welcome to my API made with FastAPI!!!",
            "name" : "neo"
        }

@app.get("/posts")
async def get_posts():
    return {"data" : "A demo post"}

@app.post("/createposts")
async def create_posts(payload: dict = Body):
    print(payload)
    return {"new_post" : f"title : {payload['title']} , content : {payload['content']}"}