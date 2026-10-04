from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Image, Post
from src.schemas import (
    HealthResponse,
    ImageCreate,
    ImageResponse,
    PostCreate,
    PostResponse,
    RootResponse,
)

router = APIRouter()


@router.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(message="FlyRank API is running")


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


def save_record(database: Session, record: Image | Post) -> None:
    try:
        database.add(record)
        database.commit()
        database.refresh(record)
    except SQLAlchemyError as error:
        database.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database operation failed",
        ) from error


@router.post(
    "/images", response_model=ImageResponse, status_code=status.HTTP_201_CREATED
)
def create_image(image: ImageCreate, database: Session = Depends(get_db)) -> Image:
    record = Image(filename=image.filename, status=image.status)
    save_record(database, record)
    return record


@router.get("/images", response_model=list[ImageResponse])
def list_images(database: Session = Depends(get_db)) -> list[Image]:
    try:
        return list(database.scalars(select(Image).order_by(Image.id)).all())
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database operation failed",
        ) from error


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, database: Session = Depends(get_db)) -> Post:
    record = Post(title=post.title, content=post.content)
    save_record(database, record)
    return record


@router.get("/posts", response_model=list[PostResponse])
def list_posts(database: Session = Depends(get_db)) -> list[Post]:
    try:
        return list(database.scalars(select(Post).order_by(Post.id)).all())
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database operation failed",
        ) from error
