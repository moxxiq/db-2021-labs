import csv
from config import datasets, output_folder, table_name
from profiler import profile_time
import database


def from_csv_to_database(table_name):
    """
    Load csv file to database. Add `year` column
    """
    for year, path in datasets.items():
        # load csv files
        with open(path, encoding='cp1251') as dataset:
            datasets[year] = csv.DictReader(dataset, delimiter=';')
            print(f"Year {year} is loading")
            database.insert_values(datasets[year], year, size=16384,
                                   collection_name=table_name)


def to_csv(collection):
    """
    Save csv file with given header and rows into output folder
    """
    with open(output_folder + 'result.csv', 'w') as result:
        result_writer = csv.DictWriter(result, fieldnames=collection[0].keys())
        result_writer.writeheader()
        result_writer.writerows(collection)
    print("Saved to csv:", len(collection), "rows")


@profile_time
def main():
    database.drop_collection(collection_name=table_name)
    try:
        from_csv_to_database(table_name=table_name)
    except (database.connection_failure, database.auto_reconnect) as e:
        print(e)
        print("Data not fully loaded. Please, try again")
        exit()
    to_csv(tuple(database.get_min_phys_2019_2020(table_name)))


if __name__ == '__main__':
    main()
