import pandas as pd
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.engine.base import Engine

from core.settings import settings
from services.helper import (
    get_request_for_upd, get_files_tables, get_tables_for_overload
)


class PortalServices:
    def __init__(self, server: SSHTunnelForwarder, portal: str) -> None:
        self.portal = portal
        self.engine = create_engine(
            settings.portals_settings[portal].mysql_db % (
                server.local_bind_port
            )
        )

    def update_table(self, file: str, table: str):
        try:
            df = pd.read_csv(file, sep=';',)
            result = df.to_sql(
                table,
                con=self.engine,
                if_exists='replace',
                index=False,
                chunksize=10000,
                )
        except Exception as e:
            return 0, str(e)
        return result, ''

    def update_tables(self):
        result = []
        success = True
        file_table = get_files_tables(self.portal)
        for file, table in file_table:
            rows, err = self.update_table(file, table)
            res = {'table': table, 'rows': rows}
            if err:
                res['error'] = err
                success = False
            result.append(
                res
            )

        return result, success

    def update_portal(self):
        with self.engine.connect() as connection:
            request = get_request_for_upd(self.portal)
            #print(request)
            try:
                result = connection.execute(text(request))
            except Exception as e:
                raise e
            return result


class EtlServices:
    def __init__(
            self,
            server_sender: SSHTunnelForwarder,
            server_recipient: SSHTunnelForwarder,
    ) -> None:
        self.engine_recipient = create_engine(
            settings.recipient.mysql_db % (server_recipient.local_bind_port)
        )
        self.engine_sender = create_engine(
            settings.sender.mysql_db % (server_sender.local_bind_port)
        )

    def get_data(self, engine: Engine, table: str):
        with engine.connect() as connection:
            source_data = connection.execute(text(f'SELECT * FROM {table};'))
            while results := source_data.fetchmany(100):
                yield results

    def overload_tables(self):
        metadata = MetaData()

        with self.engine_recipient.connect() as connection:
            for table_name in get_tables_for_overload():
                print(table_name)
                table_recipient = Table(
                    table_name, metadata, autoload_with=self.engine_recipient
                )
                result = connection.execute(text(f'TRUNCATE {table_name};'))
                for batch in self.get_data(self.engine_sender, table_name):
                    val = [bat._asdict() for bat in batch]
                    insert_stmt = table_recipient.insert().values(val)
                    connection.execute(insert_stmt)
            connection.commit()


class UpdatingPortalServis:
    def update_portal(self, portal: str) -> dict:
        result = {}
        with SSHTunnelForwarder(
            ssh_address_or_host=settings.host,
            ssh_username=settings.login,
            ssh_password=settings.password,
            remote_bind_address=(
                settings.ssh_tunnel_local_host, settings.ssh_tunnel_local_port
            )
        ) as server:
            server.start()
            portal_services = PortalServices(server, portal)
            update_tables, result_tables = portal_services.update_tables()
            result['update_tables'] = update_tables
            result['update_tables_result'] = result_tables
            if result_tables:
                try:
                    portal_services.update_portal()
                    result['update_portal'] = 'success'
                except Exception as e:
                    result['update_portal'] = str(e)
            else:
                result['update_portal'] = 'not started'
        return result

    def etl(self):

        with SSHTunnelForwarder(
                ssh_address_or_host=settings.recipient.host,
                ssh_username=settings.recipient.login,
                ssh_password=settings.recipient.password,
                remote_bind_address=(
                    settings.ssh_tunnel_local_host,
                    settings.ssh_tunnel_local_port,
                )
        ) as server_recipient, SSHTunnelForwarder(
                ssh_address_or_host=settings.sender.host,
                ssh_username=settings.sender.login,
                ssh_password=settings.sender.password,
                remote_bind_address=(
                    settings.ssh_tunnel_local_host,
                    settings.ssh_tunnel_local_port,
                )
        ) as server_sender:
            server_recipient.start()
            server_sender.start()

            etl_services = EtlServices(server_sender, server_recipient)
            return etl_services.overload_tables()


def get_portal_service():
    return UpdatingPortalServis()