import os
from pathlib import Path

import pytest

from mrt_guide.path_finder import PathFinder


class TestPathFinder:
    def test_invalid_input(self):
        data_path = (Path(
            os.path.realpath(__file__)
        ) / Path('../data/test_mrt_map.csv')).resolve()
        finder = PathFinder(data_path)
        with pytest.raises(ValueError):
            finder.find_routes('', 'CC1')
        with pytest.raises(ValueError):
            finder.find_routes('CC1', 'NO_EXISTING')
        with pytest.raises(ValueError):
            finder.find_routes('CC1', 'CC1', 'INVALID')

    def test_find_path(self):
        data_path = (Path(
            os.path.realpath(__file__)
        ) / Path('../data/test_mrt_map.csv')).resolve()
        finder = PathFinder(data_path)
        routes = finder.find_routes('NS1', 'CC5')
        assert len(routes) == 2
        assert len(routes[0][0]) == 2
        assert routes[0][1] == 0
        assert len(routes[1][0]) == 8
        assert routes[1][1] == 6
        routes = finder.find_routes('test1', 'test1')
        assert len(routes) == 2
        assert len(routes[0][0]) == 1
        assert routes[0][1] == 0
        assert len(routes[1][0]) == 1
        assert routes[1][1] == 0
        routes = finder.find_routes('test1', 'test5')
        assert len(routes) == 4
        assert len(routes[0][0]) == 6
        assert routes[0][1] == 4
        assert len(routes[1][0]) == 7
        assert routes[1][1] == 4
        assert len(routes[2][0]) == 8
        assert routes[2][1] == 6
        assert len(routes[3][0]) == 9
        assert routes[3][1] == 6
        routes = finder.find_routes('test1', 'test5', dt='2019-06-19T8:00')
        assert len(routes) == 4
        assert len(routes[0][0]) == 6
        assert routes[0][1] == 59
        assert len(routes[1][0]) == 7
        assert routes[1][1] == 74
        assert len(routes[2][0]) == 8
        assert routes[2][1] == 75
        assert len(routes[3][0]) == 9
        assert routes[3][1] == 90
        routes = finder.find_routes('test1', 'test5', limit=1)
        assert len(routes) == 1
        assert len(routes[0][0]) == 6
        assert routes[0][1] == 4
        routes = finder.find_routes(
            'test1', 'test5', dt='2019-06-19T8:00', limit=1
        )
        assert len(routes) == 1
        assert len(routes[0][0]) == 6
        assert routes[0][1] == 59
