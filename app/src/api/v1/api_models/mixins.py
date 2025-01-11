from pydantic import BaseModel, Field, UUID4


class UUIDMixin(BaseModel):
    uuid: UUID4 = Field(alias="id")
