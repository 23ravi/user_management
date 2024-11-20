import sys
from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/user_management")
from app.controllers.user import api_router as user_ns


router.include_router(user_ns, prefix="/users", tags=["User"])

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
