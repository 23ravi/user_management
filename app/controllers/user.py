from fastapi import HTTPException, APIRouter
from uuid import uuid4
from app.schema.user import User
import boto3
from uuid import uuid4


# In-memory store (replace with DynamoDB later)
db = {}
api_router = APIRouter()
# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

@api_router.post("", status_code=201)
async def create_user(user: User):
    user_id = str(uuid4())
    table.put_item(
        Item={
            "user_id": user_id,
            **user.model_dump()
        }
    )
    return {"user_id": user_id, "message": "User created successfully"}


@api_router.get("/{user_id}")
async def get_user(user_id: str):
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@api_router.put("/{user_id}")
async def update_user(user_id: str, user: User):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    db[user_id].update(user.dict())
    return {"message": "User updated successfully"}

@api_router.delete("/{user_id}")
async def delete_user(user_id: str):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    del db[user_id]
    return {"message": "User deleted successfully"}