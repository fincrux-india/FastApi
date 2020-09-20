from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def  root():
    return ("this is my first Fast API Get")

@app.get("/items/{item_id}")
async def queryParam(item_id):
    return {"Item ID is ": item_id}
