import os
from pathlib import Path

import pytest

from mrt_guide.stations_reader import StationReader


class TestStationsReader:
    def test_can_read_properly(self):
        data_path = (Path(
            os.path.realpath(__file__)
        ) / Path('../data/test_stations.csv')).resolve()
        reader = StationReader(data_path)
        station_rows = reader.read_stations()
        assert len(station_rows) == 4
        assert len(station_rows[0]) == 3
        assert station_rows[0]['Station Code'] == 'NS1'
        assert station_rows[0]['Station Name'] == 'Jurong East'
        assert station_rows[0]['Opening Date'] == '10 March 1990'

    def test_raise_value_error_with_invalid_path(self):
        data_path = (Path(
            os.path.realpath(__file__)
        ) / Path('../data/test_stations.csvno')).resolve()
        with pytest.raises(ValueError):
            StationReader(data_path)
