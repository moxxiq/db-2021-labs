import psycopg2
import psycopg2.extras
from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DBPORT, DATABASE_NETWORK
from profiler import profile_time
# type hinting
from typing import Tuple
from decimal import Decimal

# Exception
interface_error = psycopg2.InterfaceError
operational_error = psycopg2.OperationalError

connection = psycopg2.connect(
    host=DATABASE_NETWORK,
    port=DBPORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)
connection.autocommit = True


@profile_time
def get_min_phys_2019_2020(table_name) -> Tuple[Tuple[str, Decimal, Decimal], Tuple[psycopg2.extensions.Column]]:
    query = f"""
    select res2019.regname  as "Область",
           res2019.phys_min as "Фізика 2019 мінімум",
           res2020.phys_min as "Фізика 2020 мінімум"
    from (select regname, min(physball100) phys_min
           from {table_name}
           where {table_name}.physteststatus = 'Зараховано'
             and {table_name}.year = 2019
           group by {table_name}.regname) as res2019
             join
         (select regname, min(physball100) as phys_min
          from {table_name}
          where {table_name}.physteststatus = 'Зараховано'
            and {table_name}.year = 2020
          group by {table_name}.regname) as res2020
         on res2019.regname = res2020.regname
    order by "Область";
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return tuple(col.name for col in cursor.description), tuple(cursor.fetchall())
