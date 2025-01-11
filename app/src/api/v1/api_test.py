from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from services.test import TestService, get_test_service
from .api_models.api_model_test import Test

test_router = APIRouter()


@test_router.get("/{test_id}", summary="test", description="Test description.")
async def test_by_id(
    test_id: UUID4,
    test_service: TestService = Depends(get_test_service),
) -> Test:
    test = await test_service.get_by_id(test_id)
    if not test:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="test not found")
    return Test(**test.model_dump())
