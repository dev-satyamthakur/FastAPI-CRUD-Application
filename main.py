from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
            "message" : "Welcome to my API made with FastAPI!!!",
            "name" : "neo"
        }

@app.get("/posts")
def get_posts():
    return {"data" : "A demo post"}