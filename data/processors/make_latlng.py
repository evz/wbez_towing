if __name__ == "__main__":
    import sys
    import csv
    reader = csv.reader(sys.stdin)
    rows = []
    reader.next()
    for row in reader:
        loc = row[-1]
        idx1 = loc.find('(')
        idx2 = loc.find(')')
        try:
            lat, lng = [float(l) for l in loc[idx1+1:idx2].split(',')]
        except ValueError:
            lat, lng = None, None
        row.append(lat)
        row.append(lng)
        rows.append(row)
    writer = csv.writer(sys.stdout)
    writer.writerows(rows)
