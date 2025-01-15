from pydantic import BaseModel


class UpdTable(BaseModel):
    table: str
    rows: int
    error: str | None = None


class UpdPortal(BaseModel):
    upd_tables: list[UpdTable]
    upd_portal: str
