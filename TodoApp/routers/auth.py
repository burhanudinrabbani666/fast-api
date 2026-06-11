from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/auth", tags=["Auth"])
async def get_user():
    return {"user": "burhanudin"}
