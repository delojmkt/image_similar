from data.query import get_query
from utils import MysqlClient
import pandas as pd

__all__ = ["loading"]


def load_mysql(db_type) -> pd.DataFrame:
    conn = MysqlClient.get_conn(db_type)
    return pd.read_sql(get_query(), conn)


def loading(atype: str, file_path: str = None, db_type="mysql") -> pd.DataFrame:
    if atype == "mysql":
        return load_mysql(db_type)
    elif atype == "csv":
        return pd.read_csv(file_path)
    else:
        raise TypeError("loading type must be the one of csv, mysql")
