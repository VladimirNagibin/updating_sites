from http import HTTPStatus

from fastapi import APIRouter, Depends, Response  #, HTTPException
#from pydantic import UUID4

from services.portals import UpdatingPortalServis, get_portal_service
from schemas.v1.entity import UpdTable, UpdPortal

upd_portal = APIRouter()


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
