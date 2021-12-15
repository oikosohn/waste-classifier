from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List, Union, Optional, Dict, Any

from datetime import datetime

from src.model import Model

from app.model import get_model, get_config, predict_from_image_byte 

app = FastAPI()

users = []


@app.get("/")
def hello_world():
    return {'Welcome'}


class Product(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    products: List[Product] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @property
    def total(self):
        return len(self.products)

    def add_product(self, product: Product):
        if product.id in [existing_product.id for existing_product in self.products]:
            return self

        self.products.append(product)
        self.updated_at = datetime.now()
        return self


class UserUpdate(BaseModel):
    products: List[Product] = Field(default_factory=list)


class InferenceImageProduct(Product):
    name: str = "inference_image_product"
    result: Optional[List]


@app.get("/cls", description="사용자 리스트를 가져옵니다")
async def get_users() -> List[User]:
    return users


@app.get("/cls/{user_id}", description="사용자 정보를 가져옵니다")
async def get_user(user_id: UUID) -> Union[User, dict]:
    user = get_user_by_id(user_id=user_id)
    if not user:
        return {"message": "사용자 정보를 찾을 수 없습니다"}
    return user


def get_user_by_id(user_id: UUID) -> Optional[User]:
    return next((user for user in users if user.id == user_id), None)


@app.post("/cls", description="추론을 요청합니다")
async def make_user(files: List[UploadFile] = File(...),
                     model: Model = Depends(get_model),
                     config: Dict[str, Any] = Depends(get_config)):
    products = []
    for file in files:
        image_bytes = await file.read()
        inference_result = predict_from_image_byte(model=model, image_bytes=image_bytes, config=config)
        product = InferenceImageProduct(result=inference_result)
        products.append(product)

    new_users = User(products=products)
    users.append(new_users)
    return new_users


def update_user_by_id(user_id: UUID, user_update: UserUpdate) -> Optional[User]:
    """
    User 정보를 업데이트 합니다

    Args:
        user_id (UUID): user id
        user_update (UserUpdate): User Update DTO

    Returns:
        Optional[User]: 업데이트 된 User 또는 None
    """
    existing_user = get_user_by_id(user_id=user_id)
    if not existing_user:
        return

    updated_user = existing_user.copy()
    for next_product in user_update.products:
        updated_user = existing_user.add_product(next_product)

    return updated_user


@app.patch("/cls/{user_id}", description="사용자를 수정합니다")
async def update_user(user_id: UUID, user_update: UserUpdate):
    updated_user = update_user_by_id(user_id=user_id, user_update=user_update)

    if not updated_user:
        return {"message": "사용자 정보를 찾을 수 없습니다"}
    return updated_user


@app.get("/total/{user_id}", description="사용자 리퀘스트 총계를 요청합니다")
async def get_total(user_id: UUID):
    found_user = get_user_by_id(user_id=user_id)
    if not found_user:
        return {"message": "사용자 정보를 찾을 수 없습니다"}
    return found_user.total
