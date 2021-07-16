import pymongo
from pymongo.errors import ConnectionFailure, AutoReconnect
from bson.son import SON
from profiler import profile_time
# type hinting
from typing import Any, Optional, Dict, Iterator, Tuple
from decimal import Decimal

from config import (
    MONGO_INITDB_DATABASE, MONGO_INITDB_ROOT_USERNAME as MONGODB_USER,
    MONGO_INITDB_ROOT_PASSWORD as MONGODB_PASS, DBPORT, DATABASE_NETWORK
)

# Exception
connection_failure = ConnectionFailure
auto_reconnect = AutoReconnect

ball_keys = [
    'UkrBall100', 'UkrBall12', 'UkrBall', 'histBall100', 'histBall12',
    'histBall', 'mathBall100', 'mathBall12', 'mathBall', 'physBall100',
    'physBall12', 'physBall', 'chemBall100', 'chemBall12', 'chemBall',
    'bioBall100', 'bioBall12', 'bioBall', 'geoBall100', 'geoBall12',
    'geoBall', 'engBall100', 'engBall12', 'engBall', 'fraBall100',
    'fraBall12', 'fraBall', 'deuBall100', 'deuBall12', 'deuBall',
    'spaBall100', 'spaBall12', 'spaBall'
]


def convert_dict_types(record: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in record.items():
        if k in ['Birth', 'UkrAdaptScale', 'year']:
            record[k] = int(record[k])
        elif 'Ball' in k:
            record[k] = float(record[k])
    return record


def clean_and_convert(df: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    for row in df:
        for k in ball_keys:
            row[k] = row[k].replace(',', '.')
        keys_copy = tuple(row.keys())
        for k in keys_copy:
            if (len(row[k]) == 0) or (row[k] == 'null'):
                del row[k]
        row = convert_dict_types(row)
        yield row


def add_year(df: Iterator[Dict[str, Any]], year: int) -> Iterator[Dict[str, Any]]:
    for row in df:
        row["year"] = year
        yield row

# @profile_time
# def get_min_phys_2019_2020(table_name) -> Tuple[Tuple[str, Decimal, Decimal], Tuple[psycopg2.extensions.Column]]:
#     query = f"""
#     select res2019.regname  as "Область",
#            res2019.phys_min as "Фізика 2019 мінімум",
#            res2020.phys_min as "Фізика 2020 мінімум"
#     from (select regname, min(physball100) phys_min
#            from {table_name}
#            where {table_name}.physteststatus = 'Зараховано'
#              and {table_name}.year = 2019
#            group by {table_name}.regname) as res2019
#              join
#          (select regname, min(physball100) as phys_min
#           from {table_name}
#           where {table_name}.physteststatus = 'Зараховано'
#             and {table_name}.year = 2020
#           group by {table_name}.regname) as res2020
#          on res2019.regname = res2020.regname
#     order by "Область";
#     """
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         return tuple(col.name for col in cursor.description), tuple(cursor.fetchall())


@profile_time
def drop_collection(collection_name: str):
    if collection_name in db.list_collection_names():
        db[collection_name].drop()


@profile_time
def insert_values(df: Iterator[Dict[str, Any]], year: int, size=1024, collection_name='odata'):
    df = clean_and_convert(df)
    df = add_year(df, year)

    collection = db[collection_name]
    collection.insert_many(df)


@profile_time
def get_min_phys_2019_2020(collection_name: str):
    collection = db[collection_name]
    return collection.aggregate([
        {"$match": {"physTestStatus": "Зараховано"}},
        {"$group": {
            "_id": {
                "year": "$year",
                "regName": "$physPTRegName",
            },
            "Фізика мінімум": {"$min": "$physBall100"}
        }},
        {"$group": {
            "_id": "$_id.regName",
            "results": {
                "$push": {"k": {"$concat": ["Фізика мінімум ", "$_id.year"]}, "v": "$Фізика мінімум"}
            }
        }},
        {"$project": {
            "Область": "$_id",
            "_id": 0,
            "results": {"$arrayToObject": "$results"},
        }},
        {"$replaceRoot": {"newRoot": {"$mergeObjects": [{"Область": "$Область"}, "$results"]}}},
    ])


client = pymongo.MongoClient(
    host=DATABASE_NETWORK,
    port=DBPORT,
    username=MONGODB_USER,
    password=MONGODB_PASS,
)

try:
    # Availability check
    client.admin.command('ismaster')
except ConnectionFailure:
    print("Server not available")
    exit()

db = client[MONGO_INITDB_DATABASE]
