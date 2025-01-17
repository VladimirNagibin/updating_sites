from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class SettingsPortal(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="portal_",
                                      env_file_encoding='utf-8')
    user_db: str
    password_db: str
    name_db: str

    @property
    def mysql_db(self):
        return (f'mysql://{self.user_db}:{self.password_db}@'
                f'{settings.ssh_tunnel_local_host}:%d/{self.name_db}')


class SettingsOrnam(SettingsPortal):
    model_config = SettingsConfigDict(env_prefix="ornam_",
                                      env_file_encoding='utf-8')


class SettingsButic(SettingsPortal):
    model_config = SettingsConfigDict(env_prefix="butic_",
                                      env_file_encoding='utf-8')


class SettingsIsmy(SettingsPortal):
    model_config = SettingsConfigDict(env_prefix="ismy_",
                                      env_file_encoding='utf-8')


class SettingsRecipient(SettingsPortal):
    model_config = SettingsConfigDict(env_prefix="recipient_",
                                      env_file_encoding='utf-8')
    host: str
    login: str
    password: str


class SettingsSender(SettingsPortal):
    model_config = SettingsConfigDict(env_prefix="sender_",
                                      env_file_encoding='utf-8')
    host: str
    login: str
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "project"
    APP_RELOAD: bool = False

    host: str
    login: str
    password: str

    ssh_tunnel_local_host: str = '127.0.0.1'
    ssh_tunnel_local_port: int = 3306
    portals_settings: dict = {
        'ornam': SettingsOrnam(),
        'butic': SettingsButic(),
        'ismy': SettingsIsmy(),
    }

    sender: SettingsSender = SettingsSender()
    recipient: SettingsRecipient = SettingsRecipient()


settings = Settings()
