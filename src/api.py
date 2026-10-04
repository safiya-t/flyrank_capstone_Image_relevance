from fastapi import APIRouter

from src.schemas import HealthResponse, RootResponse

router = APIRouter()


@router.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(message="FlyRank API is running")


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
