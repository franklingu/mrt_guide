from datetime import datetime

import pytest

from mrt_guide.weights import (
    SimpleWeights, NightWeights, NormalWeights,
    PeakHourWeights, WeightsFactory
)
from mrt_guide.station import Station
from mrt_guide.exceptions import DoNotOperateException


def get_station(code, name='test'):
    return Station(code, name)


class TestWeights:
    def test_weights_factory(self):
        weight = WeightsFactory.get_weights(False)
        assert isinstance(weight, SimpleWeights)
        weight = WeightsFactory.get_weights(
            True, datetime(2019, 6, 19, 12)
        )
        assert isinstance(weight, NormalWeights)
        weight = WeightsFactory.get_weights(
            True, datetime(2019, 6, 19, 6)
        )
        assert isinstance(weight, PeakHourWeights)
        weight = WeightsFactory.get_weights(
            True, datetime(2019, 6, 19, 9)
        )
        assert isinstance(weight, NormalWeights)
        weight = WeightsFactory.get_weights(
            True, datetime(2019, 6, 19, 18)
        )
        assert isinstance(weight, PeakHourWeights)
        weight = WeightsFactory.get_weights(
            True, datetime(2019, 6, 19, 21)
        )
        assert isinstance(weight, NormalWeights)
        weight = WeightsFactory.get_weights(
            True, datetime(2019, 6, 19, 5)
        )
        assert isinstance(weight, NightWeights)
        weight = WeightsFactory.get_weights(
            True, datetime(2019, 6, 22, 18)
        )
        assert isinstance(weight, NormalWeights)

    def test_simple_weights(self):
        weights = SimpleWeights()
        assert weights.get_transfer_cost(
            get_station('EW21'), get_station('CC22')
        ) == 0
        assert weights.get_direct_cost(
            get_station('EW21'), get_station('EW22')
        ) == 1

    def test_normal_weights(self):
        weights = NormalWeights()
        assert weights.get_transfer_cost(
            get_station('EW21'), get_station('CC22')
        ) == 10
        assert weights.get_direct_cost(
            get_station('EW21'), get_station('EW22')
        ) == 10
        assert weights.get_direct_cost(
            get_station('DT21'), get_station('DT22')
        ) == 8
        assert weights.get_direct_cost(
            get_station('TE21'), get_station('TE22')
        ) == 8

    def test_night_weights(self):
        weights = NightWeights()
        assert weights.get_transfer_cost(
            get_station('EW21'), get_station('CC22')
        ) == 10
        with pytest.raises(DoNotOperateException):
            weights.get_transfer_cost(
                get_station('DT21'), get_station('EW22')
            )
        with pytest.raises(DoNotOperateException):
            weights.get_transfer_cost(
                get_station('CG21'), get_station('EW22')
            )
        with pytest.raises(DoNotOperateException):
            weights.get_transfer_cost(
                get_station('CE21'), get_station('EW22')
            )
        assert weights.get_direct_cost(
            get_station('EW21'), get_station('EW22')
        ) == 10
        assert weights.get_direct_cost(
            get_station('TE21'), get_station('TE22')
        ) == 8
        with pytest.raises(DoNotOperateException):
            weights.get_transfer_cost(
                get_station('DT21'), get_station('DT22')
            )
        with pytest.raises(DoNotOperateException):
            weights.get_transfer_cost(
                get_station('CG21'), get_station('CG22')
            )
        with pytest.raises(DoNotOperateException):
            weights.get_transfer_cost(
                get_station('CE21'), get_station('CE22')
            )

    def test_peak_hour_weights(self):
        weights = PeakHourWeights()
        assert weights.get_transfer_cost(
            get_station('EW21'), get_station('CC22')
        ) == 15
        assert weights.get_direct_cost(
            get_station('NS21'), get_station('NS22')
        ) == 12
        assert weights.get_direct_cost(
            get_station('NE21'), get_station('NE22')
        ) == 12
        assert weights.get_direct_cost(
            get_station('EW21'), get_station('EW22')
        ) == 10
