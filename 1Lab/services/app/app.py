import csv
from config import datasets, output_folder
from profiler import profile_time
import database


def from_csv_to_database():
    """
    Load csv file to database. Add `year` column
    """
    for year, path in datasets.items():
        # load csv files
        with open(path, encoding='cp1251') as dataset:
            datasets[year] = csv.DictReader(dataset, delimiter=';')
            print(f"Завантажується рік {year}")
            database.copy_dataframe(datasets[year], year)


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
    database.create_table(drop_if_exists=True)
    from_csv_to_database()
    to_csv(*database.get_min_phys_2019_2020())


if __name__ == '__main__':
    main()
