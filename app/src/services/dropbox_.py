import os
from functools import lru_cache

import dropbox
import requests
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from fastapi import Depends

from services.storage import get_storage, State
# when running locally, importing settings does not work ((
from core.settings import settings


class DropboxService:
    def __init__(self):
        pass

    @staticmethod
    def authorize() -> None:
        storage = get_storage()
        auth_flow = DropboxOAuth2FlowNoRedirect(
            settings.dropbox_app_key,  # put real key for local exec
            settings.dropbox_app_secret,  # put real secret for local exec
            token_access_type='offline',
        )

        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)

        storage.set_state('access_token', oauth_result.access_token)
        storage.set_state('refresh_token', oauth_result.refresh_token)

    @staticmethod
    def check_auth_token(state: State) -> bool:
        with dropbox.Dropbox(
            oauth2_access_token=state.get_state('access_token')
        ) as dbx:
            try:
                dbx.users_get_current_account()
                return True
            except Exception:
                return False

    @staticmethod
    def get_auth_token_by_refresh(state: State) -> int:

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': state.get_state('refresh_token'),
            'client_id': settings.dropbox_app_key,
            'client_secret': settings.dropbox_app_secret
        }
        try:
            response = requests.post(settings.dropbox_token_url, data=data)
        except Exception:
            return 500
        status_code = response.status_code
        if status_code == 200:
            token_data = response.json()
            state.set_state('access_token', token_data['access_token'])
        #  else:
        #    print("Ошибка:", response.status_code, response.text)
        return status_code

    @staticmethod
    def put_file(
        local_file_path: str, dropbox_file_path: str, state: State
    ) -> bool:
        with dropbox.Dropbox(
            oauth2_access_token=state.get_state('access_token')
        ) as dbx:
            try:
                with open(local_file_path, 'rb') as f:
                    dbx.files_upload(
                        f.read(),
                        dropbox_file_path,
                        mode=dropbox.files.WriteMode.overwrite,
                    )
                    print(f"Файл {local_file_path} успешно загружен в Dropbox "
                          f"по пути {dropbox_file_path}")
            except dropbox.exceptions.ApiError as e:
                print(f"Ошибка при загрузке файла: {e}")
                return False
        return True

    @staticmethod
    def del_file(
        dropbox_file_path: str, state: State
    ) -> bool:
        with dropbox.Dropbox(
            oauth2_access_token=state.get_state('access_token')
        ) as dbx:
            try:
                dbx.files_delete_v2(dropbox_file_path)
            except dropbox.exceptions.ApiError as e:
                print(f"Ошибка при загрузке файла: {e}")
                return False
        return True

    @staticmethod
    def upd_portal_dropbox(
        state: State
    ) -> bool:
        if not DropboxService.check_auth_token(state):
            DropboxService.get_auth_token_by_refresh(state)
        if not DropboxService.check_auth_token(state):
            return False
        result = True
        with dropbox.Dropbox(
            oauth2_access_token=state.get_state('access_token')
        ) as dbx:
            for portal, dropbox_path in settings.portals_dropbox:
                for ind in range(1, 4):
                    local_file_path = state.get_state(
                        f'{portal}_fa{ind}_active'
                    )
                    local_file = local_file_path.rsplit("/")[-1]
                    dropbox_file_path = f'{dropbox_path}{local_file}'
                    try:
                        with open(local_file_path, 'rb') as f:
                            dbx.files_upload(
                                f.read(), dropbox_file_path,
                                mode=dropbox.files.WriteMode.overwrite
                            )

                            dropbox_file_path_old = state.get_state(
                                f'{portal}_fa{ind}_dropbox'
                            )
                            try:
                                dbx.files_delete_v2(dropbox_file_path_old)
                            except dropbox.exceptions.ApiError as e:
                                print(f'Ошибка при удалении файла: {e}')
                            file_old = dropbox_file_path_old.rsplit('/')[-1]
                            try:
                                os.remove(f'data/prices/{file_old}')
                                print(f'Файл {file_old} успешно удален.')
                            except FileNotFoundError:
                                print(f'Файл {file_old} не найден.')
                            except PermissionError:
                                print(
                                    'Нет прав на удаление файла '
                                    f'{file_old}.'
                                )
                            except Exception as e:
                                print(f"Произошла ошибка: {e}")

                            state.set_state(
                                f'{portal}_fa{ind}_dropbox',
                                dropbox_file_path,
                            )
                            print(f"Файл {local_file_path} успешно загружен "
                                  f"по пути {dropbox_file_path}")
                    except dropbox.exceptions.ApiError as e:
                        print(f"Ошибка при загрузке файла: {e}")
                        result = False
        return result


@lru_cache()
def get_dropbox() -> DropboxService:
    return DropboxService()
