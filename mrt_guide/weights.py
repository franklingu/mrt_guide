'''Represent weights/minutes to take to complete commute or transfer
'''
from .exceptions import DoNotOperateException


SECONDS_IN_HOUR = 3600


class WeightsFactory:
    '''Factory to get the wanted weights representation
    '''
    @staticmethod
    def get_weights(complex_cost=False, dt=None):
        if not complex_cost or dt is None:
            return SimpleWeights()
        diff = dt - dt.replace(hour=0, minute=0, second=0, microsecond=0)
        hour_in_day = diff.total_seconds() / SECONDS_IN_HOUR
        is_at_peak = (
            0 <= dt.weekday() < 5 and
            (6 <= hour_in_day < 9 or 18 <= hour_in_day < 21)
        )
        is_at_night = (
            0 <= hour_in_day < 6 or
            22 <= hour_in_day < 24
        )
        if is_at_peak:
            return PeakHourWeights()
        elif is_at_night:
            return NightWeights()
        else:
            return NormalWeights()


class Weights:
    def __init__(self):
        pass

    def get_transfer_cost(self, station, transfer):
        raise NotImplementedError('To be implemented')

    def get_direct_cost(self, station, neighbor):
        raise NotImplementedError('To be implemented')


class SimpleWeights(Weights):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_transfer_cost(self, station, transfer):
        return 0

    def get_direct_cost(self, station, transfer):
        return 1


class PeakHourWeights(Weights):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.peak_busy = set(['NS', 'NE'])
        self.peak_busy_wait = 12
        self.peak_wait = 10
        self.peak_transfer = 15

    def get_transfer_cost(self, station, transfer):
        return self.peak_transfer

    def get_direct_cost(self, station, neighbor):
        if (station.line in self.peak_busy and
                neighbor.line in self.peak_busy):
            return self.peak_busy_wait
        return self.peak_wait


class NightWeights(Weights):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.night_stop = set(['DT', 'CG', 'CE'])
        self.night_fast = set(['TE'])
        self.night_transfer = 10
        self.night_fast_wait = 8
        self.night_wait = 10

    def get_transfer_cost(self, station, transfer):
        if station.line in self.night_stop:
            raise DoNotOperateException()
        elif transfer.line in self.night_stop:
            raise DoNotOperateException()
        return self.night_transfer

    def get_direct_cost(self, station, neighbor):
        if station.line in self.night_stop:
            raise DoNotOperateException()
        elif neighbor.line in self.night_stop:
            raise DoNotOperateException()
        if (station.line in self.night_fast and
                neighbor.line in self.night_fast):
            return self.night_fast_wait
        return self.night_wait


class NormalWeights(Weights):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normal_fast = set(['DT', 'TE'])
        self.normal_fast_wait = 8
        self.normal_wait = 10
        self.normal_transfer = 10

    def get_transfer_cost(self, station, transfer):
        return self.normal_transfer

    def get_direct_cost(self, station, neighbor):
        if (station.line in self.normal_fast and
                neighbor.line in self.normal_fast):
            return self.normal_fast_wait
        return self.normal_wait
