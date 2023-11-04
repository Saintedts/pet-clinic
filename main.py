from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    error_detail = []
    for error in exc.errors():
        error_detail.append({
            "loc": [str(x) for x in error.get("loc")],
            "msg": error.get("msg"),
            "type": error.get("type")
        })
    return JSONResponse(content={"detail": error_detail}, status_code=422)


@app.get('/')
def root():
    return 'Successful Response'


@app.post("/post")
def create_post(new_post: Timestamp):
    post_db.append(new_post)
    return new_post


@app.get('/dog')
def get_dogs(kind: str):
    dogs_list = [dog for dog in dogs_db.values() if dog.kind == kind]

    if len(dogs_list) == 0:
        raise HTTPException(status_code=422, detail="No dogs this kind")
    return {'response': dogs_list}


@app.post("/dog")
def create_dog(dog: Dog):
    new_id = max(dogs_db.keys()) + 1
    dog.pk = new_id
    dogs_db[new_id] = dog
    return {'response': dogs_db[new_id]}


@app.get('/dog/{pk}')
def get_dog(pk: int):

    if pk not in dogs_db.keys():
        raise HTTPException(status_code=422, detail="No dog for this id")

    dog = dogs_db[pk]
    return dog


@app.patch("/dog/{pk}")
def update_dog(pk: int, name: str, kind: str):
    dogs_db[pk].name = name
    dogs_db[pk].kind = kind
    return {'response': dogs_db[pk]}
