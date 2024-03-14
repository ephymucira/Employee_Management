from fastapi import FastAPI, Body, Request,Form,UploadFile,File
import shutil
import uvicorn
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates  = Jinja2Templates(directory = "templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class student(BaseModel):
    id:str
    name:str
    subject: List[str] = []


@app.get('/')
async def home():
    return{'message':'hello fastAPI'}

@app.get('/hello/{name}/{age}')
async def Hello(name: str, age: int):
    return {f'My name is {name} and am {age} years old'}


@app.post('/students')
async def student_data(s1: student):
    return s1

@app.post("/students_data")
async def student_data(name:str=Body(...), marks:int=Body(...)):
    return{"name":name, "marks":marks}

@app.get("/templates")
async def my_templates():
    temp = """
<html>
<head></head>
<body>
<p>Hello world<p>
</body>
</html>


"""
    return HTMLResponse(content=temp)

@app.get("/hello/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello.html", {"request":request})


@app.get("/items/{id}/", response_class=HTMLResponse)
async def read_item(request: Request, id:str):
    user_id = id
    return templates.TemplateResponse(request=request, name="hello.html", context={"user_id": user_id})


@app.get('/weuh/{name}')
async def weuh(request: Request, name: str):
    return templates.TemplateResponse("index.html", {"request": request, "name":name})


@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/submit/")
async def submit(nm: str = Form(...), pwd: str = Form(...)):
    return {"username": nm}

@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/uploader/")
async def create_upload_file(file: UploadFile =  File(...)):
    with open("destination.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename }












if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)    
