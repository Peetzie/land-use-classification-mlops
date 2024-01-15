import re
import torch
from enum import Enum
from http import HTTPStatus
from typing import Optional

import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from project import CNN

app = FastAPI()


@app.get("/")
def read_root():
    """Simple root endpoint."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """Simple function to get an item by id."""
    return {"item_id": item_id}


class ItemEnum(Enum):
    """Item enum."""

    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/restric_items/{item_id}")
def read_item(item_id: ItemEnum):  # noqa: F811
    """Simple function to get an item by id."""
    return {"item_id": item_id}


@app.get("/query_items")
def read_item(item_id: int):  # noqa: F811
    """Simple function to get an item by id."""
    return {"item_id": item_id}


database = {"username": [], "password": []}


@app.post("/login/")
def login(username: str, password: str):
    """Simple function to save a login."""
    username_db = database["username"]
    password_db = database["password"]
    if username not in username_db and password not in password_db:
        with open("database.csv", "a") as file:
            file.write(f"{username}, {password} \n")
        username_db.append(username)
        password_db.append(password)
    return "login saved"


@app.get("/text_model/")
def contains_email(data: str):
    """Simple function to check if an email is valid."""
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    response = {
        "input": data,
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "is_email": re.fullmatch(regex, data) is not None,
    }
    return response


class DomainEnum(Enum):
    """Domain enum."""

    gmail = "gmail"
    hotmail = "hotmail"


class Item(BaseModel):
    """Item model."""

    email: str
    domain: DomainEnum


@app.post("/text_model/")
def contains_email_domain(data: Item):
    """Simple function to check if an email is valid."""
    if data.domain is DomainEnum.gmail:
        regex = r"\b[A-Za-z0-9._%+-]+@gmail+\.[A-Z|a-z]{2,}\b"
    if data.domain is DomainEnum.hotmail:
        regex = r"\b[A-Za-z0-9._%+-]+@hotmail+\.[A-Z|a-z]{2,}\b"
    response = {
        "input": data,
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "is_email": re.fullmatch(regex, data.email) is not None,
    }
    return response


@app.post("/cv_model/")
async def cv_model(data: UploadFile, out_path: Optional[str] = '', h: Optional[int] = 256, w: Optional[int] = 256):
    """Simple function using open-cv to resize an image."""
    with open(out_path + 'image.png', "wb") as image:
        content = await data.read()
        image.write(content)
        image.close()
    # model = CNN()

    img = cv2.imread(out_path + "image.png")
    # img_tensor = torch.tensor(img)
    # pred = torch.argmax(model(img_tensor))

    res = cv2.resize(img, (h, w))
    cv2.imwrite(out_path + "image_resize.png", res)

    response = {
        "input": data,
        "output": FileResponse(out_path + "image_resize.png"),
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        # "pred": pred
    }
    return response
