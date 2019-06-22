from collections import OrderedDict

import pytest

from mrt_guide.mrt_map import MRTMap


class MockedSimpleWeight:
    def __init__(self):
        pass

    def get_transfer_cost(self, start, end):
        return 0

    def get_direct_cost(self, start, end):
        return 1


class MockedNormalWeight:
    def __init__(self):
        self.normal_fast = ['DT', 'TE']

    def get_transfer_cost(self, start, end):
        return 10

    def get_direct_cost(self, start, end):
        if start.line in self.normal_fast or end.line in self.normal_fast:
            return 8
        return 10


def get_station_row(row):
    names = ['Station Code', 'Station Name', 'Opening Date']
    result = OrderedDict()
    for name, val in zip(names, row):
        result[name] = val
    return result


class TestMRTMap:
    def test_invalid_station(self):
        mrt_map = MRTMap([
            get_station_row(['NS1', 'test1', '10 March 1990']),
            get_station_row(['NS2', 'test2', '10 March 1990']),
        ])
        with pytest.raises(ValueError):
            mrt_map.find_routes('NO_EXISTING', 'NS1', MockedSimpleWeight())
        with pytest.raises(ValueError):
            mrt_map.find_routes('NS1', 'NO_EXISTING', MockedSimpleWeight())

    def test_same_start_end(self):
        mrt_map = MRTMap([
            get_station_row(['NS1', 'test1', '10 March 1990']),
            get_station_row(['NS2', 'test2', '10 March 1990']),
            get_station_row(['TE1', 'test1', '10 March 1990']),
            get_station_row(['TE2', 'test3', '10 March 1990']),
            get_station_row(['TE3', 'test4', '10 March 1990']),
        ])
        routes = mrt_map.find_routes('NS1', 'NS1', MockedSimpleWeight())
        assert len(routes) == 1
        assert len(routes[0][0]) == 1
        assert routes[0][1] == 0
        routes = mrt_map.find_routes('NS1', 'TE1', MockedSimpleWeight())
        assert len(routes) == 1
        assert len(routes[0][0]) == 2
        assert routes[0][1] == 0

    def test_with_cycle(self):
        mrt_map = MRTMap([
            get_station_row(['NS1', 'test1', '10 March 1990']),
            get_station_row(['NS2', 'test2', '10 March 1990']),
            get_station_row(['TE1', 'test1', '10 March 1990']),
            get_station_row(['TE2', 'test3', '10 March 1990']),
            get_station_row(['CC1', 'test3', '10 March 1990']),
            get_station_row(['DT1', 'test3', '10 March 1990']),
            get_station_row(['TE3', 'test2', '10 March 1990']),
            get_station_row(['TE4', 'test4', '10 March 1990']),
        ])
        routes = mrt_map.find_routes('NS1', 'NS2', MockedSimpleWeight())
        assert len(routes) == 2
        assert len(routes[0][0]) == 2
        assert routes[0][1] == 1
        assert len(routes[1][0]) == 5
        assert routes[1][1] == 2
        routes = mrt_map.find_routes('test1', 'test2', MockedSimpleWeight())
        assert len(routes) == 4
        # shortest path
        assert len(routes[0][0]) == 2
        assert routes[0][1] == 1
        # start from another station code for start
        assert len(routes[1][0]) == 3
        assert routes[1][1] == 1
        # take a circle
        assert len(routes[2][0]) == 3
        assert routes[2][1] == 2
        # start from another station code for start
        assert len(routes[3][0]) == 4
        assert routes[3][1] == 2
        routes = mrt_map.find_routes('NS1', 'test4', MockedSimpleWeight())
        assert len(routes) == 2
        assert len(routes[0][0]) == 4
        assert routes[0][1] == 2
        assert len(routes[1][0]) == 5
        assert routes[1][1] == 3

    def test_with_cycle_and_complex_weights(self):
        mrt_map = MRTMap([
            get_station_row(['NS1', 'test1', '10 March 1990']),
            get_station_row(['NS2', 'test2', '10 March 1990']),
            get_station_row(['TE1', 'test1', '10 March 1990']),
            get_station_row(['TE2', 'test3', '10 March 1990']),
            get_station_row(['CC1', 'test3', '10 March 1990']),
            get_station_row(['DT1', 'test3', '10 March 1990']),
            get_station_row(['TE3', 'test2', '10 March 1990']),
            get_station_row(['TE4', 'test4', '10 March 1990']),
        ])
        routes = mrt_map.find_routes('NS1', 'NS2', MockedNormalWeight())
        assert len(routes) == 2
        assert len(routes[0][0]) == 2
        assert routes[0][1] == 10
        assert len(routes[1][0]) == 5
        assert routes[1][1] == 36
        routes = mrt_map.find_routes('test1', 'test2', MockedNormalWeight())
        assert len(routes) == 4
        # shortest path
        assert len(routes[0][0]) == 2
        assert routes[0][1] == 10
        # start from another station code for start
        assert len(routes[1][0]) == 3
        assert routes[1][1] == 16
        # take a circle
        assert len(routes[2][0]) == 3
        assert routes[2][1] == 20
        # start from another station code for start
        assert len(routes[3][0]) == 4
        assert routes[3][1] == 26
        routes = mrt_map.find_routes('NS1', 'test4', MockedNormalWeight())
        assert len(routes) == 2
        assert len(routes[0][0]) == 4
        assert routes[0][1] == 28
        assert len(routes[1][0]) == 5
        assert routes[1][1] == 34

    def test_without_cycle(self):
        mrt_map = MRTMap([
            get_station_row(['NS1', 'test1', '10 March 1990']),
            get_station_row(['NS2', 'test2', '10 March 1990']),
            get_station_row(['NS3', 'test3', '10 March 1990']),
            get_station_row(['CC1', 'test3', '10 March 1990']),
            get_station_row(['DT1', 'test3', '10 March 1990']),
            get_station_row(['CC2', 'test4', '10 March 1990']),
        ])
        routes = mrt_map.find_routes('NS1', 'CC2', MockedSimpleWeight())
        assert len(routes) == 1
        assert len(routes[0][0]) == 5
        assert routes[0][1] == 3

    def test_with_limit(self):
        mrt_map = MRTMap([
            get_station_row(['NS1', 'test1', '10 March 1990']),
            get_station_row(['NS2', 'test2', '10 March 1990']),
            get_station_row(['TE1', 'test1', '10 March 1990']),
            get_station_row(['TE2', 'test3', '10 March 1990']),
            get_station_row(['CC1', 'test3', '10 March 1990']),
            get_station_row(['DT1', 'test3', '10 March 1990']),
            get_station_row(['TE3', 'test2', '10 March 1990']),
            get_station_row(['TE4', 'test4', '10 March 1990']),
            get_station_row(['CG1', 'testn', '10 March 1990']),
        ])
        routes = mrt_map.find_routes(
            'NS1', 'NS2', MockedSimpleWeight(), limit=1
        )
        assert len(routes) == 1
        routes = mrt_map.find_routes(
            'NS1', 'CG1', MockedSimpleWeight(), limit=1
        )
        assert len(routes) == 0
