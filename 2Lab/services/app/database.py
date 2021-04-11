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
    with results as
             (select regname, year, min(ball100) as phys_min
              from test
                       join participant on participant.outid = test.outid
                       join place on participant.placeid = place.placeid
              where status = 'Зараховано'
                and name = 'Фізика'
              group by regname, year)
    select r19.regname as "Область", r19.phys_min as "Фізика 2019 мінімум", r20.phys_min as "Фізика 2020 мінімум"
    from (select regname, phys_min from results where year = 2019) as r19
             join (select regname, phys_min from results where year = 2020) as r20
                  on r19.regname = r20.regname;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return tuple(col.name for col in cursor.description), tuple(cursor.fetchall())
