from fastapi import APIRouter

from src.user.api import user_router
from src.student.api import student_router

# Router
api_router = APIRouter()

# User
api_router.include_router(user_router, include_in_schema=True, tags=["User APIs"])
api_router.include_router(student_router, include_in_schema=True, tags=["Student APIs"])
