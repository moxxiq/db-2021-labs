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
            # database.copy_dataframe(datasets[year], year, size=32768)
            database.exec_values(datasets[year], year, size=32768, table_name=table_name)


def to_csv(header, rows):
    """
    Save csv file with given header and rows into output folder
    """
    with open(output_folder + 'result.csv', 'w') as result:
        result_writer = csv.writer(result, delimiter=';')
        result_writer.writerow(header)
        result_writer.writerows(rows)


@profile_time
def main():
    database.create_table(table_name=table_name, drop_if_exists=False)
    try:
        from_csv_to_database(table_name=table_name)
    except (database.interface_error, database.operational_error) as e:
        print(e)
        print("Data not fully loaded. Please, try again")
        exit()
    to_csv(*database.get_min_phys_2019_2020(table_name))


if __name__ == '__main__':
    main()
