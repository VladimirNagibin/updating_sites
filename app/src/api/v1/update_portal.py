from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from services.portals import UpdatingPortalServis, get_portal_service
from schemas.v1.entity import EtlTable, UpdTable, UpdPortal

upd_portal = APIRouter()


@upd_portal.get(
        "/etl", summary="reload portal", description="Reload portals."
    )
def reload_port(
    response: Response,
    page: int | None = None,
    upd_service: UpdatingPortalServis = Depends(get_portal_service),
) -> EtlTable:
    result = upd_service.etl(page)
    print(result)
    if result.get('error'):
        response.status_code = HTTPStatus.BAD_REQUEST
    return EtlTable(**result)


@upd_portal.get(
        "/{portal}", summary="updating portal", description="Updating portals."
    )
def upt_port(
    portal: str,
    response: Response,
    upd_service: UpdatingPortalServis = Depends(get_portal_service),
) -> UpdPortal:
    result = upd_service.update_portal(portal)
    upd_tables = [UpdTable(**res) for res in result['update_tables']]
    upd_portal = result['update_portal']
    if (upd_portal != 'success') or (not result['update_tables_result']):
        response.status_code = HTTPStatus.BAD_REQUEST
    return UpdPortal(upd_tables=upd_tables, upd_portal=upd_portal)
