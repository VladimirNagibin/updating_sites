import os
from http import HTTPStatus

from fastapi import APIRouter, File, HTTPException, UploadFile

upload_file_router = APIRouter()


@upload_file_router.post(
        "/upload",
        summary="upload file",
        description="Upload file by the path.",
    )
async def upload_file(path: str, file: UploadFile = File(...)):
    try:
        os.mkdir(f"data/{path}")
        print(os.getcwd())
    except Exception as e:
        print(e)
    try:
        contents = file.file.read()
        with open(f"data/{path}/{file.filename}", "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Something went wrong',
        )
    finally:
        file.file.close()

    return {"result": HTTPStatus.OK}
