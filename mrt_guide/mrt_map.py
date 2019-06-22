'''Represent the MRTMap, which is essentially a graph of Stations

MRTMap stores all the Station as node and connection between stations
as edge. One special thing in addition is the handling of interchange
stations. Interchange stations are identified by taking out different
station codes with the same station name. The core part of path seeking
is built on top of the variantion of Dijkstra's algorithm. The graph
could be weighted/unweighted depending on the configuration.

`MRTMap.find_routes` will try to find as many routes as possible without
considering loops. This is to allow downstream to do different kind of
processing based on their needs.

`MRTMap` does not assume things about constructor param `station_rows`
and with some filtering on input `station_rows`, `MRTMap` can easily
deal with Singapore MRT map back into the past or into the future by filtering
out stations that are built yet by some point of time.
'''
from collections import defaultdict
from functools import total_ordering
import heapq

from .station import Station
from .exceptions import DoNotOperateException


@total_ordering
class StationItem:
    def __init__(self, cost, station, route, prev_stations):
        self.cost = cost
        self.count = len(route)
        self.station = station
        self.route = route
        self.prev_stations = prev_stations

    def invalid(self):
        return self.station in self.prev_stations

    def to_next(self, weight, next_station):
        return StationItem(
            self.cost + weight,
            next_station,
            self.route + [self.station],
            self.prev_stations.union(set([self.station]))
        )

    def __eq__(self, other):
        return (self.cost, self.count) == (other.cost, other.count)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.cost, self.count) < (other.cost, other.count)


class MRTMap:
    def __init__(self, station_rows):
        station_name_map = defaultdict(set)
        station_code_map = {}
        transfers = defaultdict(set)
        neighbors = defaultdict(set)
        lines = defaultdict(list)
        for station_row in station_rows:
            code = station_row['Station Code']
            name = station_row['Station Name']
            station = Station(code, name)
            station_name_map[name].add(station)
            station_code_map[code] = station
            lines[station.line].append(station)
        # fill in transfer information
        for stations in station_name_map.values():
            stations = list(stations)
            for i, station1 in enumerate(stations):
                for j, station2 in enumerate(stations):
                    if i == j:
                        continue
                    transfers[station1].add(station2)
        # construct neighbors information
        for stations in lines.values():
            stations.sort(key=lambda x: x.index)
            for i, station in enumerate(stations):
                if i > 0:
                    prev_station = stations[i - 1]
                    neighbors[station].add(prev_station)
                    neighbors[prev_station].add(station)
                if i < len(stations) - 1:
                    next_station = stations[i + 1]
                    neighbors[station].add(next_station)
                    neighbors[next_station].add(station)
        self.station_name_map = station_name_map
        self.station_code_map = station_code_map
        self.transfers = transfers
        self.neighbors = neighbors

    def map_to_stations(self, param):
        if param in self.station_code_map:
            return set([self.station_code_map[param]])
        elif param in self.station_name_map:
            return self.station_name_map[param]
        raise ValueError('{} is not a valid station'.format(param))

    def find_routes(self, start, end, weights, limit=None):
        '''Find routes from start to end ranked by cost

        Makes use of Dijkistra algorithm and in particular all cycles
        are of sum which is larger than 0. So for any route, there is no
        point checking back on a visited station.
        There are two parts to be take into consideration: cost so far
        and steps so far. Two are combined as the weight of the route
        covered so far. Graph is connected and no negative cycles are
        present. The algorithm will always explore shorter paths so far
        and exhaust all possible options if needed.
        '''
        start = self.map_to_stations(start)
        end = self.map_to_stations(end)
        pq = [(StationItem(0, station, [], set())) for station in start]
        routes = []
        while pq:
            station_item = heapq.heappop(pq)
            if station_item.invalid():
                continue
            station = station_item.station
            if station in end:
                routes.append((
                    station_item.route + [station], station_item.cost
                ))
                # if limit is specified and met, stop the search
                if limit is not None and len(routes) >= limit:
                    break
                continue
            connections = self.find_connections(station, weights)
            for next_station, weight in connections:
                if next_station in station_item.prev_stations:
                    continue
                # Do not take the same hot transfer station if not
                # to take transfer to another line
                if (next_station.name == station.name and
                        station_item.route and
                        station_item.route[-1].name == station.name):
                    continue
                heapq.heappush(
                    pq,
                    station_item.to_next(weight, next_station),
                )
        return routes

    def find_connections(self, station, weights):
        for transfer in self.transfers.get(station, []):
            try:
                yield transfer, weights.get_transfer_cost(station, transfer)
            except DoNotOperateException:
                pass
        for neighbor in self.neighbors.get(station, []):
            try:
                yield neighbor, weights.get_direct_cost(station, neighbor)
            except DoNotOperateException:
                pass
