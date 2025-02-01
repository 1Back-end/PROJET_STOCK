from fastapi import APIRouter
from .migration_controller import router as migration
from .user_controller import router as user
from .category_controller import router as category
from .products_controller import router as product
from .storage_controller import router as storage

api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(user)
api_router.include_router(category)
api_router.include_router(product)
api_router.include_router(storage)