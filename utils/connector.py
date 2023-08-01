import settings
import pymysql

__all__ = ["MysqlClient"]


class MysqlClient(object):
    mysql_conn = settings.mysql

    def get_conn(db_type: str):
        return pymysql.connect(**MysqlClient.mysql_conn)
