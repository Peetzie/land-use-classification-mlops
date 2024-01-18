import re
import os
from enum import Enum
from http import HTTPStatus
from typing import Optional
from pathlib import Path

import numpy as np
from io import BytesIO
from PIL import Image
import torch
import wandb
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
async def cv_model(
    data: UploadFile, out_path: Optional[str] = "", n: Optional[int] = 5
):
    img = np.array(Image.open(BytesIO(await data.read())))

    wandb.login(key="7d4f6c7fcf5702feb08b64a3f24e850a3f66a5b5")
    run = wandb.init(project='land-use-classification')
    artifact = run.use_artifact('fabcult/land-use-classification/model-1xmu70qt:latest', type='model')
    artifact_dir = artifact.download()
    model = CNN.load_from_checkpoint(Path(artifact_dir) / 'model.ckpt')

    img_tensor = torch.tensor(img, dtype=torch.float32).reshape(torch.Size([1, model.channels, model.img_dim, model.img_dim]))
    logits = model(img_tensor).squeeze()
    pred = torch.argsort(logits, descending=True).squeeze()[:n]

    class_dict = {
        0: "agricultural",
        1: "airplane",
        2: "baseballdiamond",
        3: "beach",
        4: "buildings",
        5: "chaparral",
        6: "denseresidential",
        7: "forest",
        8: "freeway",
        9: "golfcourse",
        10: "intersection",
        11: "mediumresidential",
        12: "mobilehomepark",
        13: "overpass",
        14: "parkinglot",
        15: "river",
        16: "runway",
        17: "sparseresidential",
        18: "storagetanks",
        19: "tenniscourt",
        20: "harbor",
    }

    response = {
        "input": data,
        "output": FileResponse(out_path + "image_resize.png"),
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "probability_dictionary": {class_dict[el.item()]: logits[el].item() for el in pred},
    }
    return response
