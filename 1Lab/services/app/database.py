import psycopg2
import psycopg2.extras
from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DBPORT, DATABASE_NETWORK
from profiler import profile_time
import io
import re
from itertools import islice
from math import ceil
# type hinting
from typing import Any, Optional, Dict, Iterator, Tuple
from decimal import Decimal

# Exception
interface_error = psycopg2.InterfaceError
operational_error = psycopg2.OperationalError

table_columns_types = {
    "OUTID": "varchar(36) PRIMARY KEY",
    "Birth": "smallint",
    "SEXTYPENAME": "sex",
    "REGNAME": "TEXT",
    "AREANAME": "TEXT",
    "TERNAME": "TEXT",
    "REGTYPENAME": "TEXT",
    "TerTypeName": "ter",
    "ClassProfileNAME": "TEXT",
    "ClassLangName": "TEXT",
    "EONAME": "TEXT",
    "EOTYPENAME": "TEXT",
    "EORegName": "TEXT",
    "EOAreaName": "TEXT",
    "EOTerName": "TEXT",
    "EOParent": "TEXT",
    "UkrTest": "TEXT",
    "UkrTestStatus": "TEXT",
    "UkrBall100": "numeric",
    "UkrBall12": "numeric",
    "UkrBall": "numeric",
    "UkrAdaptScale": "numeric",
    "UkrPTName": "TEXT",
    "UkrPTRegName": "TEXT",
    "UkrPTAreaName": "TEXT",
    "UkrPTTerName": "TEXT",
    "histTest": "TEXT",
    "HistLang": "TEXT",
    "histTestStatus": "TEXT",
    "histBall100": "numeric",
    "histBall12": "numeric",
    "histBall": "numeric",
    "histPTName": "TEXT",
    "histPTRegName": "TEXT",
    "histPTAreaName": "TEXT",
    "histPTTerName": "TEXT",
    "mathTest": "TEXT",
    "mathLang": "TEXT",
    "mathTestStatus": "TEXT",
    "mathBall100": "numeric",
    "mathBall12": "numeric",
    "mathBall": "numeric",
    "mathPTName": "TEXT",
    "mathPTRegName": "TEXT",
    "mathPTAreaName": "TEXT",
    "mathPTTerName": "TEXT",
    "physTest": "TEXT",
    "physLang": "TEXT",
    "physTestStatus": "TEXT",
    "physBall100": "numeric",
    "physBall12": "numeric",
    "physBall": "numeric",
    "physPTName": "TEXT",
    "physPTRegName": "TEXT",
    "physPTAreaName": "TEXT",
    "physPTTerName": "TEXT",
    "chemTest": "TEXT",
    "chemLang": "TEXT",
    "chemTestStatus": "TEXT",
    "chemBall100": "numeric",
    "chemBall12": "numeric",
    "chemBall": "numeric",
    "chemPTName": "TEXT",
    "chemPTRegName": "TEXT",
    "chemPTAreaName": "TEXT",
    "chemPTTerName": "TEXT",
    "bioTest": "TEXT",
    "bioLang": "TEXT",
    "bioTestStatus": "TEXT",
    "bioBall100": "numeric",
    "bioBall12": "numeric",
    "bioBall": "numeric",
    "bioPTName": "TEXT",
    "bioPTRegName": "TEXT",
    "bioPTAreaName": "TEXT",
    "bioPTTerName": "TEXT",
    "geoTest": "TEXT",
    "geoLang": "TEXT",
    "geoTestStatus": "TEXT",
    "geoBall100": "numeric",
    "geoBall12": "numeric",
    "geoBall": "numeric",
    "geoPTName": "TEXT",
    "geoPTRegName": "TEXT",
    "geoPTAreaName": "TEXT",
    "geoPTTerName": "TEXT",
    "engTest": "TEXT",
    "engTestStatus": "TEXT",
    "engBall100": "numeric",
    "engBall12": "numeric",
    "engDPALevel": "TEXT",
    "engBall": "numeric",
    "engPTName": "TEXT",
    "engPTRegName": "TEXT",
    "engPTAreaName": "TEXT",
    "engPTTerName": "TEXT",
    "fraTest": "TEXT",
    "fraTestStatus": "TEXT",
    "fraBall100": "numeric",
    "fraBall12": "numeric",
    "fraDPALevel": "TEXT",
    "fraBall": "numeric",
    "fraPTName": "TEXT",
    "fraPTRegName": "TEXT",
    "fraPTAreaName": "TEXT",
    "fraPTTerName": "TEXT",
    "deuTest": "TEXT",
    "deuTestStatus": "TEXT",
    "deuBall100": "numeric",
    "deuBall12": "numeric",
    "deuDPALevel": "TEXT",
    "deuBall": "numeric",
    "deuPTName": "TEXT",
    "deuPTRegName": "TEXT",
    "deuPTAreaName": "TEXT",
    "deuPTTerName": "TEXT",
    "spaTest": "TEXT",
    "spaTestStatus": "TEXT",
    "spaBall100": "numeric",
    "spaBall12": "numeric",
    "spaDPALevel": "TEXT",
    "spaBall": "numeric",
    "spaPTName": "TEXT",
    "spaPTRegName": "TEXT",
    "spaPTAreaName": "TEXT",
    "spaPTTerName": "TEXT",
    "year": "smallint",
}


def clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return 'null'
    # replace decimal separator from comma to point
    dec_sep = re.compile(r'^\s*(\d+)\,(\d+)\s*$')
    return dec_sep.sub(
        r'\1.\2',
        str(value).replace('\n', '\\n'))


def make_csv(df: Iterator[Dict[str, Any]], year: int) -> io.StringIO:
    csv_file = io.StringIO()
    for row in df:
        # print('|'.join(map(clean_csv_value, (*row.values(), year)))
        #       + '\n')
        csv_file.write('|'.join(map(clean_csv_value, (*row.values(), year)))
                       + '\n')
    csv_file.seek(0)
    return csv_file


connection = psycopg2.connect(
    host=DATABASE_NETWORK,
    port=DBPORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)
connection.autocommit = True


@profile_time
def create_table(drop_if_exists=True) -> None:
    """
    Create table with prepared structure
    """
    additional_types_query = """DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sex') THEN
                CREATE TYPE sex AS ENUM ('жіноча', 'чоловіча');
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ter') THEN
                CREATE TYPE ter AS ENUM ('місто', 'село');
            END IF;
        END
        $$;"""

    odata_drop_query = "DROP TABLE IF EXISTS odata;"

    odata_create_query = "CREATE TABLE IF NOT EXISTS odata ("
    odata_create_query += ", ".join(f'{col} {t}' for col, t in table_columns_types.items())
    odata_create_query += ");"
    with connection.cursor() as cursor:
        cursor.execute(additional_types_query)
        if drop_if_exists:
            cursor.execute(odata_drop_query)
        cursor.execute(odata_create_query)


@profile_time
def copy_dataframe(df: Iterator[Dict[str, Any]], year: int):
    csv_file_like_object = make_csv(df, year)
    with connection.cursor() as cursor:
        cursor.copy_from(csv_file_like_object, 'odata', sep='|', null='null')


@profile_time
def get_min_phys_2019_2020() -> Tuple[Tuple[str, Decimal, Decimal], Tuple[psycopg2.extensions.Column]]:
    query = """
    select res2019.regname  as "Область",
           res2019.phys_min as "Фізика 2019 мінімум",
           res2020.phys_min as "Фізика 2020 мінімум"
    from (select regname, min(physball100) phys_min
           from odata
           where odata.physteststatus = 'Зараховано'
             and odata.year = 2019
           group by odata.regname) as res2019
             join
         (select regname, min(physball100) as phys_min
          from odata
          where odata.physteststatus = 'Зараховано'
            and odata.year = 2020
          group by odata.regname) as res2020
         on res2019.regname = res2020.regname
    order by "Область";
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return tuple(col.name for col in cursor.description), tuple(cursor.fetchall())
