from fastapi import APIRouter
from .migration_controller import router as migration
from .user_controller import router as user


api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(user)
