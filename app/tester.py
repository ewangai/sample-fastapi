
from fastapi import FastAPI

#create instance of FastAPI
app = FastAPI()

#Path operation or Route
@app.get("/")                           # Decorator - This turns htis into an path operator to the endpoint is usable e.b. a get method plus path
async def root():                       # Function - async is optional but required when asynchronous task (takes time) name of the function here is root but it can be anything. root is default
    return {"message": "Yep all good"}
