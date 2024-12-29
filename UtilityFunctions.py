import csv

def csv_to_image_array(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    data = [int(cell) if ',' not in cell else tuple(map(int, cell.split(','))) for row in data[1:] for cell in row]
    
    return data