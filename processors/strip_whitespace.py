if __name__ == "__main__":
    import sys
    import csv
    import re
    reader = csv.reader(sys.stdin)
    rows = []
    for row in reader:
        for idx, val in enumerate(row):
            row[idx] = re.sub('\s+', ' ', row[idx])
        rows.append(row)
    writer = csv.writer(sys.stdout)
    writer.writerows(rows)
