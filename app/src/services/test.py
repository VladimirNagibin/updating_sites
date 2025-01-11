import uuid
from functools import lru_cache

from pydantic import UUID4

from models.model_test import Test


class TestRepository:
    def __init__(self): ...

    async def get_test_by_id(self, genre_id: UUID4) -> Test | None:
        try:
            doc = {"id": str(uuid.uuid4()), "name": "name"}
            return Test(**doc)
        except Exception:
            return None


class TestService:
    def __init__(self, repository: TestRepository):
        self.repository = repository

    async def get_by_id(self, test_id: UUID4) -> Test | None:
        return await self.repository.get_test_by_id(test_id)


@lru_cache()
def get_test_service() -> TestService:
    repository = TestRepository()
    return TestService(repository)
