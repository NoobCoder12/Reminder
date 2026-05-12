# __init__.py makes Python treat this folder as a module
# This file runs automatically when you import the api/v1 folder
# It aggregates all routers - when you have multiple endpoint files
# you can collect them here into one router and import in main.py as:
# from api.v1 import api_router

from fastapi import APIRouter

from app.api.v1 import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router)