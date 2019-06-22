from mrt_guide.station import Station


class TestStation:
    def test_construction(self):
        station = Station('NS1', 'Jurong East')
        assert station.line == 'NS'
        assert station.index == 1
        assert station.code == 'NS1'
        assert station.name == 'Jurong East'
        assert str(station) == 'Station[NS1,Jurong East]'

    def test_hashable(self):
        station1 = Station('NS1', 'Jurong East')
        station2 = Station('NS1', 'Jurong East')
        assert set([station1]) == set([station2])
