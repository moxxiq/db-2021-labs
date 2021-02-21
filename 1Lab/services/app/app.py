import csv
from config import datasets
from profiler import profile_time
from database import create_table


@profile_time
def main():
    create_table()

    for year, path in datasets.items():
        # load csv files
        with open(path, encoding='cp1251') as dataset:
            datasets[year] = csv.DictReader(dataset, delimiter=';')
            # just print header (keys of the dictionary)
            print(tuple(next(datasets[year])))


if __name__ == '__main__':
    main()
