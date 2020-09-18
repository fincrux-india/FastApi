from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def  root():
    return ("this is my first Fast API Get")