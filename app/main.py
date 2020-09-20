from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel
app=FastAPI()

@app.get("/")
async def  root():
    return ("this is my first Fast API Get")

@app.get("/items/{item_id}")
async def queryParam(item_id : int):
    return {"Item ID is ": item_id}

#in case we want to pass pareameters with data type
#async def queryParam(item_id : int); if you pass string the error comes : 
# {"detail":[{"loc":["path","item_id"],"msg":"value is not a valid integer","type":"type_error.integer"}]}

# All the data validation under hood is done by 'Pydantic'

# Creating a Enum class
from enum import Enum
class ModelName(str, Enum):
    rahul="rahul"
    isha="isha"
    pranjay="Pranjay"


@app.get('/model/{model_name}')
async def get_model(model_name:ModelName):
    if model_name==ModelName.rahul:
        return {"model name": model_name,"message":" Rahul How are you?"}
    if model_name==ModelName.isha:
            return {"model name": model_name,"message":" Isha How are you?"}
    if model_name==ModelName.pranjay:
            return {"model name": model_name,"message":" Pranjay How are you?"}


#Request and Response Body

class Item(BaseModel):
    name: str
    description:Optional[str]=None
    price:float
    tax: Optional[float]=None

# Request Body + Query Parameter+ Additional Valiadtion using Query
@app.post("/item/{item_id}")
async def create_item(item:Item,q:Optional[str]=Query(None, max_length=50, min_length=2, regex=r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")):
    item_dict=item.dict()
    if item.tax:
        itemWithTax= item.price+item.tax
        item_dict.update({"itemwithtax": itemWithTax})
    if q:
        item_dict.update({"q":q})
    return item_dict


