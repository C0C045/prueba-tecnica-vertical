from fastapi import APIRouter, Query, status
from ..services import external_api

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_external_data():
    return external_api.get_posts()

@router.get("/filter", status_code=status.HTTP_200_OK)
def filter_external_data(user_id: int = Query(None, description="Filtra por userId")):
    data = external_api.get_posts()
    if user_id:
        data = [post for post in data if post["userId"] == user_id]
    return data
