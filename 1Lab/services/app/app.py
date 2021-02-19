import psycopg2
import os


def list_files(startpath):
    # copy-pastle
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        yield '{}{}/'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            yield '{}{}'.format(subindent, f)


def main():
    print("I'm working")
    with open('../output/struct.txt', 'w') as f:
        f.write("\n".join(list_files('/data/')))


if __name__ == '__main__':
    main()
