from fastapi import APIRouter, Query
from ..services import external_api

router = APIRouter()

@router.get("/")
def get_external_data():
    return external_api.get_posts()

@router.get("/filter")
def filter_external_data(user_id: int = Query(None, description="Filtra por userId")):
    data = external_api.get_posts()
    if isinstance(data, dict) and "error" in data:
        return data
    if user_id:
        data = [post for post in data if post["userId"] == user_id]
    return data
