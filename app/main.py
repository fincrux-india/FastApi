from fastapi import FastAPI

app=FastAPI()

@app.add("/")
async def  root():
    return ("this is my first Fast API Get")