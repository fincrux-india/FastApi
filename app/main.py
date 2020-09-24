from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel

import requests
import pdfplumber
import regex as re
import pandas as pd

from io import StringIO
import json
#import DataFrame

app=FastAPI()

# @app.get("/")
# async def  root():
#     return ("Welcome to Fincrux")

# @app.get("/items/{item_id}")
# async def queryParam(item_id : int):
#     return {"Item ID is ": item_id}

#in case we want to pass pareameters with data type
#async def queryParam(item_id : int); if you pass string the error comes : 
# {"detail":[{"loc":["path","item_id"],"msg":"value is not a valid integer","type":"type_error.integer"}]}

# All the data validation under hood is done by 'Pydantic'

# Creating a Enum class
# from enum import Enum
# class ModelName(str, Enum):
#     rahul="rahul"
#     isha="isha"
#     pranjay="Pranjay"


# @app.get('/model/{model_name}')
# async def get_model(model_name:ModelName):
#     if model_name==ModelName.rahul:
#         return {"model name": model_name,"message":" Rahul How are you?"}
#     if model_name==ModelName.isha:
#             return {"model name": model_name,"message":" Isha How are you?"}
#     if model_name==ModelName.pranjay:
#             return {"model name": model_name,"message":" Pranjay How are you?"}


#Request and Response Body

# class Item(BaseModel):
#     name: str
#     description:Optional[str]=None
#     price:float
#     tax: Optional[float]=None

# Request Body + Query Parameter+ Additional Valiadtion using Query
# ... is called ellipsis and placing it as a first parameter tells FastAPI that this value is required
# @app.post("/item/{item_id}")
# async def create_item(item:Item,q:Optional[str]=Query(..., max_length=50, min_length=2, regex=r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")):
#     item_dict=item.dict()
#     if item.tax:
#         itemWithTax= item.price+item.tax
#         item_dict.update({"itemwithtax": itemWithTax})
#     if q:
#         item_dict.update({"q":q})
#     return item_dict

def download_file(url):
    local_filename=url.split('/')[-1]
    with requests.get(url) as r:
        with open(local_filename,'wb') as f:
            f.write(r.content)
    return local_filename


@app.get("/cams/")
async def cams_parser(pdf_url:Optional[str]=None):
    #pdf_file=download_file(pdf_url)

    
    file='data/cams.pdf'
    with pdfplumber.open(file) as pdf:
        page=pdf.pages[1]
        #text=page.extract_text()
        table=page.extract_table()
    
    df = pd.DataFrame(table[1:], columns=table[0])
    columns=['Folio No', 'Scheme Name', 'Closing Units', 'Valuation(`)']
    
    if set(columns).issubset(df.columns):
        
        for column in ['Folio No', 'Scheme Name', 'Closing Units', 'Valuation(`)']:
            df[column] = df[column].str.replace('\n', '$')

        patternDel = "[0-9]"
        #filter = df[df['Folio No'].str.contains(patternDel)]
 
        df1=df.loc[df['Folio No'].str.contains(patternDel)]

        df1.rename(columns={'Folio No': 'Folio', 'Scheme Name': 'Scheme', 'Closing Units':'Units', 'NAV(`)':'NAV','Cost Value (`)':'Value','Valuation(`)':'Valuation'}, inplace=True)
        
        df1['Units']=df1["Units"].str.split("$")
        df1['Valuation']=df1["Valuation"].str.split('$')
        df1['Folio']=df1["Folio"].str.split('$')
        df1['NAV']=df1["NAV"].str.split('\n')
        df1['Value']=df1["Value"].str.split('\n')


        df1['Scheme']=df1["Scheme"].str.split('$',1)
        df1=df1.apply(pd.Series.explode)
        df1.reset_index(drop=True, inplace=True)

        pattern = '[A-Z][$]'
    
        for i in df1.index:
            row=df1.loc[i,'Scheme']
            series=pd.Series(row)
            count=len(re.findall(pattern,series.to_string(index = False)))
    
            if count==1:

                str1= df1.loc[i,'Scheme'].split('$')
                df1.loc[i,'Scheme']=str1
                df1.loc[i, 'Scheme'] = str1[1]

 
        d = df1.to_dict(orient='records')
        return d
