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
    "UkrAdaptScale": "int",
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

ball_keys = [
    'UkrBall100', 'UkrBall12', 'UkrBall', 'histBall100', 'histBall12',
    'histBall', 'mathBall100', 'mathBall12', 'mathBall', 'physBall100',
    'physBall12', 'physBall', 'chemBall100', 'chemBall12', 'chemBall',
    'bioBall100', 'bioBall12', 'bioBall', 'geoBall100', 'geoBall12',
    'geoBall', 'engBall100', 'engBall12', 'engBall', 'fraBall100',
    'fraBall12', 'fraBall', 'deuBall100', 'deuBall12', 'deuBall',
    'spaBall100', 'spaBall12', 'spaBall'
]

def clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return 'null'
    # replace decimal separator from comma to point
    dec_sep = re.compile(r'^\s*(\d+)\,(\d+)\s*$')
    return dec_sep.sub(
        r'\1.\2',
        str(value).replace('\n', '\\n'))


def make_csv(df: Iterator[Dict[str, Any]], year: int) -> io.StringIO:
    """
    Make streaming string with corrections from csv.DictReader dataset
    """
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
def create_table(table_name='odata', drop_if_exists=True) -> None:
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

    odata_drop_query = f"DROP TABLE IF EXISTS {table_name};"

    odata_create_query = "CREATE TABLE IF NOT EXISTS odata ("
    odata_create_query += ", ".join(f'{col} {t}' for col, t in table_columns_types.items())
    odata_create_query += ");"
    with connection.cursor() as cursor:
        cursor.execute(additional_types_query)
        if drop_if_exists:
            cursor.execute(odata_drop_query)
        cursor.execute(odata_create_query)


@profile_time
def copy_dataframe(df: Iterator[Dict[str, Any]], year: int, size=1024):
    csv_file_like_object = make_csv(df, year)
    with connection.cursor() as cursor:
        cursor.copy_from(csv_file_like_object, 'odata', sep='|', null='null', size=size)


def clean_dict_df(df: Iterator[Dict[str, Any]]) -> Iterator[Tuple[str]]:
    for row in df:
        for k in ball_keys:
            row[k] = row[k].replace(',', '.')
        for k, v in row.items():
            if len(v) == 0 or v == 'null':
                row[k] = None
        yield tuple(row.values())


@profile_time
def exec_values(df: Iterator[Dict[str, Any]], year: int, size=1024, table_name='odata'):
    year_count = {
        '2019': 353813,
        '2020': 379299
    }
    year_count_query = f"select count(*) from {table_name} where year = {str(year)};"
    query = f"insert into {table_name} values %s ON CONFLICT DO NOTHING;"
    template = "(" + ", ".join(['%s'] * (len(table_columns_types) - 1)) + f", {str(year)})"
    cleaned_df_values = clean_dict_df(df)
    with connection.cursor() as cursor:
        # if all records of current year is present, we skip insertion
        cursor.execute(year_count_query)
        count = cursor.fetchone()[0]
        # considering inserting with permanent `batch` size, regarding wrong lines in csv
        if count == year_count.get(year):
            return
        else:
            blocks_to_skip = ceil(count / size) * size
            print(f"Skiping existing blocks {blocks_to_skip}, existing count = {count}")
            cleaned_df_values = islice(cleaned_df_values, blocks_to_skip, None)

        psycopg2.extras.execute_values(
            cur=cursor,
            sql=query,
            argslist=cleaned_df_values,
            template=template,
            page_size=size
        )


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
