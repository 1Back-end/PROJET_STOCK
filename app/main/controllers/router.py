from fastapi import APIRouter


from .migration_controller import router as migration


api_router = APIRouter()

api_router.include_router(migration)
