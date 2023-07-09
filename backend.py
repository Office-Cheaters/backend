from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated
import os
import json

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

import uuid

import sys
sys.path.append("/home/ubuntu")

from model import Model

app = FastAPI()

@app.get("/api/v1/helloworld")
def helloworld():
    print("helloworld")
    return "helloworld"


@app.post("/api/v1/prompt")
def prompt(    prompt: Annotated[str, Form()],
    file: Annotated[UploadFile, File()]):
    # Model Class 선언
    model = Model()

    myuuid = uuid.uuid4()

    createDirectory(f"/home/ubuntu/upload/{myuuid}/")

    file_location = f"/home/ubuntu/upload/{myuuid}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # data랑 prompt 넣고 함수 호출
    output = model.request(file_location, prompt)

    print("\n\nwoojin", output)

    if output['answer'] is not None:
        try:
            output['answer'] = {'type': 'json', 'data':json.loads(output['answer'].to_json())}
        except:
            output['answer'] = {'type': str(type(output['answer']).__name__), 'data':output['answer']}
        output['file'] = None
    else:
        output['file'] = {'extension': "png",'url':"https://of.fice.kro.kr/static/"+output['uuid']+"/output.png" }

    return output