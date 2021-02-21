import psycopg2
from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, DBPORT, DATABASE_NETWORK
from profiler import profile_time

connection = psycopg2.connect(
    host=DATABASE_NETWORK,
    port=DBPORT,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)
connection.autocommit = True


@profile_time
def create_table():
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

    table_columns_types = {
        "OUTID": "varchar(36)",
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
        "UkrBall100": "smallint",
        "UkrBall12": "smallint",
        "UkrBall": "smallint",
        "UkrAdaptScale": "numeric",
        "UkrPTName": "TEXT",
        "UkrPTRegName": "TEXT",
        "UkrPTAreaName": "TEXT",
        "UkrPTTerName": "TEXT",
        "histTest": "TEXT",
        "HistLang": "TEXT",
        "histTestStatus": "TEXT",
        "histBall100": "smallint",
        "histBall12": "smallint",
        "histBall": "smallint",
        "histPTName": "TEXT",
        "histPTRegName": "TEXT",
        "histPTAreaName": "TEXT",
        "histPTTerName": "TEXT",
        "mathTest": "TEXT",
        "mathLang": "TEXT",
        "mathTestStatus": "TEXT",
        "mathBall100": "smallint",
        "mathBall12": "smallint",
        "mathBall": "smallint",
        "mathPTName": "TEXT",
        "mathPTRegName": "TEXT",
        "mathPTAreaName": "TEXT",
        "mathPTTerName": "TEXT",
        "physTest": "TEXT",
        "physLang": "TEXT",
        "physTestStatus": "TEXT",
        "physBall100": "smallint",
        "physBall12": "smallint",
        "physBall": "smallint",
        "physPTName": "TEXT",
        "physPTRegName": "TEXT",
        "physPTAreaName": "TEXT",
        "physPTTerName": "TEXT",
        "chemTest": "TEXT",
        "chemLang": "TEXT",
        "chemTestStatus": "TEXT",
        "chemBall100": "smallint",
        "chemBall12": "smallint",
        "chemBall": "smallint",
        "chemPTName": "TEXT",
        "chemPTRegName": "TEXT",
        "chemPTAreaName": "TEXT",
        "chemPTTerName": "TEXT",
        "bioTest": "TEXT",
        "bioLang": "TEXT",
        "bioTestStatus": "TEXT",
        "bioBall100": "smallint",
        "bioBall12": "smallint",
        "bioBall": "smallint",
        "bioPTName": "TEXT",
        "bioPTRegName": "TEXT",
        "bioPTAreaName": "TEXT",
        "bioPTTerName": "TEXT",
        "geoTest": "TEXT",
        "geoLang": "TEXT",
        "geoTestStatus": "TEXT",
        "geoBall100": "smallint",
        "geoBall12": "smallint",
        "geoBall": "smallint",
        "geoPTName": "TEXT",
        "geoPTRegName": "TEXT",
        "geoPTAreaName": "TEXT",
        "geoPTTerName": "TEXT",
        "engTest": "TEXT",
        "engTestStatus": "TEXT",
        "engBall100": "smallint",
        "engBall12": "smallint",
        "engDPALevel": "TEXT",
        "engBall": "smallint",
        "engPTName": "TEXT",
        "engPTRegName": "TEXT",
        "engPTAreaName": "TEXT",
        "engPTTerName": "TEXT",
        "fraTest": "TEXT",
        "fraTestStatus": "TEXT",
        "fraBall100": "smallint",
        "fraBall12": "smallint",
        "fraDPALevel": "TEXT",
        "fraBall": "smallint",
        "fraPTName": "TEXT",
        "fraPTRegName": "TEXT",
        "fraPTAreaName": "TEXT",
        "fraPTTerName": "TEXT",
        "deuTest": "TEXT",
        "deuTestStatus": "TEXT",
        "deuBall100": "smallint",
        "deuBall12": "smallint",
        "deuDPALevel": "TEXT",
        "deuBall": "smallint",
        "deuPTName": "TEXT",
        "deuPTRegName": "TEXT",
        "deuPTAreaName": "TEXT",
        "deuPTTerName": "TEXT",
        "spaTest": "TEXT",
        "spaTestStatus": "TEXT",
        "spaBall100": "smallint",
        "spaBall12": "smallint",
        "spaDPALevel": "TEXT",
        "spaBall": "smallint",
        "spaPTName": "TEXT",
        "spaPTRegName": "TEXT",
        "spaPTAreaName": "TEXT",
        "spaPTTerName": "TEXT",
        "year": "smallint",
    }

    odata_drop_query = "DROP TABLE IF EXISTS odata;"

    odata_create_query = "CREATE TABLE odata ("
    odata_create_query += ", ".join(f'{col} {t}' for col, t in table_columns_types.items())
    odata_create_query += ");"
    with connection.cursor() as cursor:
        cursor.execute(additional_types_query)
        cursor.execute(odata_drop_query)
        cursor.execute(odata_create_query)
