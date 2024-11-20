from fastapi import HTTPException, APIRouter
from uuid import uuid4
from app.schema.user import User
import boto3
from botocore.exceptions import ClientError
from uuid import uuid4


# In-memory store (replace with DynamoDB later)
db = {}
api_router = APIRouter()
# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
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
def get_user(user_id: str):
    try:
        response = table.get_item(Key={"id": user_id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="User not found")
        return response["Item"]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/{user_id}")
def update_user(user_id: str, user: User):
    try:
        table.update_item(
            Key={"id": user_id},
            UpdateExpression="set firstname=:f, lastname=:l, dob=:d, address=:a, gender=:g, email=:e, phone_number=:p",
            ExpressionAttributeValues={
                ":f": user.firstname,
                ":l": user.lastname,
                ":d": user.dob,
                ":a": user.address,
                ":g": user.gender,
                ":e": user.email,
                ":p": user.phone_number,
            }
        )
        return {"message": "User updated successfully"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete("/{user_id}")
def delete_user(user_id: str):
    try:
        table.delete_item(Key={"id": user_id})
        return {"message": "User deleted successfully"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
