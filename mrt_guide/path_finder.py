'''A simple wrapper for connecting input reader with MRTMap
'''
from datetime import datetime

from .stations_reader import StationReader
from .mrt_map import MRTMap
from .weights import WeightsFactory


class PathFinder:
    def __init__(
            self,
            data_path,
            reader_cls=StationReader,
            weights_factory=WeightsFactory):
        '''Glue logic needed to read input into graph and seek path

        data_path: data file path
        reader_cls: default StationReader, customize if needed
        weights_factory: default WeightsFactory, customize if needed
        '''
        station_rows = reader_cls(data_path).read_stations()
        mrt_map = MRTMap(station_rows)
        self.mrt_map = mrt_map
        self.weights_factory = weights_factory

    def find_routes(self, start, end, dt=None, limit=None):
        '''Find path between start and end
        '''
        if dt is None:
            return self.mrt_map.find_routes(
                start, end, self.weights_factory.get_weights(), limit=limit,
            )
        try:
            dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M')
        except ValueError:
            raise ValueError('Malformatted datetime: {}'.format(datetime))
        return self.mrt_map.find_routes(
            start,
            end,
            self.weights_factory.get_weights(True, dt),
            limit=limit,
        )
