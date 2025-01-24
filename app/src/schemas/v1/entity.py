from pydantic import BaseModel


class UpdTable(BaseModel):
    table: str
    rows: int
    error: str | None = None


class UpdPortal(BaseModel):
    upd_tables: list[UpdTable]
    upd_portal: str


class EtlTable(BaseModel):
    tables: list[str]
    page: int | None
    upd: bool
    error: str | None = None


class ExportTable(BaseModel):
    part: int
    result: int | None = None
    file: str | None = None
    error: str | None = None
