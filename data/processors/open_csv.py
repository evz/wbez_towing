if __name__ == "__main__":
    import sys
    import csv
    fname = sys.argv[1]
    reader = csv.reader(open(fname, 'rb'))
    rows = list(reader)
    writer = csv.writer(sys.stdout)
    writer.writerows(rows)
