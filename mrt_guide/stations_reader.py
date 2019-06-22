'''Read input data into memory
'''
import csv
from pathlib import Path


class StationReader:
    def __init__(self, data_path):
        data_path = Path(data_path)
        if not data_path.exists():
            raise ValueError('Invalid file path provided')
        self.data_path = data_path

    def read_stations(self):
        stations = []
        with open(self.data_path, 'r') as ifile:
            reader = csv.DictReader(ifile)
            for row in reader:
                stations.append(row)
        return stations
