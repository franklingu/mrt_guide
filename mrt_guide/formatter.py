'''Collection of built-in formatters

All formatters will inherit from Formatter class. And for any
future extension to the package or self extension to formatters,
simply inherit from Formatter and register with use of `regiester_formatter'
decorator.
'''


_formatters = {}


def register_formatter(formatter_type):
    def wrapper(cls):
        if formatter_type in _formatters:
            raise ValueError(
                'The formatter type {} has been taken'.format(formatter_type)
            )
        _formatters[formatter_type] = cls
        return cls
    return wrapper


class FormatterFactory:
    @staticmethod
    def get_formatter(formatter_type=None):
        if formatter_type is None:
            return ConsoleFormatter()
        return _formatters.get(formatter_type, ConsoleFormatter)()


class Formatter:
    def __init__(self):
        pass

    def format_routes(self, start, end, routes, simple=True, limit=1):
        raise NotImplementedError('To be implemented')


@register_formatter('console')
class ConsoleFormatter(Formatter):
    def __init__(self):
        super().__init__()

    def format_routes(self, start, end, routes, simple=True, limit=1):
        if len(routes) == 0:
            return 'No available route find between {} and {}'.format(
                start, end
            )
        results = [
            'Recommended routes between {} and {}'.format(start, end)
        ]
        for index in range(min(limit, len(routes))):
            route = routes[index]
            results.extend(self.format_route(route, simple))
            results.append('\n\n')
        return '\n'.join(results)

    def format_route(self, route, simple):
        prev = None
        stations, cost = route
        results = []
        if not simple:
            results.append('The estimated time: {} mins'.format(cost))
        for station in stations:
            if not prev:
                prev = station
                continue
            if prev.line == station.line:
                results.append('Take {} line from {} to {}'.format(
                    station.line, prev, station
                ))
            else:
                results.append('Transfer to {} line'.format(
                    station.line
                ))
            prev = station
        return results
