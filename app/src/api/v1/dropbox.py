import os
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from services.dropbox_ import DropboxService, get_dropbox
from services.storage import get_storage, State

dropbox_router = APIRouter()


@dropbox_router.get(
        "/check-token",
        summary="check auth token",
        description="Check auth token.",
    )
def check_token(
    response: Response,
    dropbox_service: DropboxService = Depends(get_dropbox),
    state: State = Depends(get_storage),
) -> bool:
    result = dropbox_service.check_auth_token(state)
    if not result:
        response.status_code = HTTPStatus.BAD_REQUEST
    return result


@dropbox_router.get(
        "/upd-token",
        summary="update auth token",
        description="Update auth token by refresh token.",
    )
def upd_token(
    response: Response,
    dropbox_service: DropboxService = Depends(get_dropbox),
    state: State = Depends(get_storage),
) -> int:
    result = dropbox_service.get_auth_token_by_refresh(state)
    if result != 200:
        response.status_code = result
    return result


@dropbox_router.get(
        "/upd_portal_dropbox",
        summary="update portal dropbox",
        description="Update prices in dropbox.",
    )
def upd_portal_dropbox(
    response: Response,
    dropbox_service: DropboxService = Depends(get_dropbox),
    state: State = Depends(get_storage),
) -> bool:
    result = dropbox_service.upd_portal_dropbox(state)
    if not result:
        response.status_code = HTTPStatus.BAD_REQUEST
    return True
