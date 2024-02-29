import csv

def parse_csv(input_file, output_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Time', 'Latitude', 'Longitude', 'Intensity'])
            for row in reader:
                if len(row) < 6:
                    continue  # Skip rows that don't have enough elements
                date = row[0]
                time = row[1]
                lat_str = row[4]
                lon_str = row[5]
                if lat_str.endswith('N'):
                    lat = float(lat_str[:-1])
                elif lat_str.endswith('S'):
                    lat = -float(lat_str[:-1])
                else:
                    continue  # Skip rows with invalid latitude format
                if lon_str.endswith('E'):
                    lon = float(lon_str[:-1])
                elif lon_str.endswith('W'):
                    lon = -float(lon_str[:-1])
                else:
                    continue  # Skip rows with invalid longitude format
                intensity = int(row[6])
                writer.writerow([f"{date} {time}", lat, lon, intensity])


# Input and output file names
input_file = 'example2.csv'
output_file = 'example21.csv'

# Parse CSV and generate results
parse_csv(input_file, output_file)