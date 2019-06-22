from mrt_guide.station import Station
from mrt_guide.formatter import (
    FormatterFactory, ConsoleFormatter
)


class TestFormatter:
    def test_formatter_factory(self):
        formatter = FormatterFactory.get_formatter()
        assert isinstance(formatter, ConsoleFormatter)
        formatter = FormatterFactory.get_formatter('console')
        assert isinstance(formatter, ConsoleFormatter)
        formatter = FormatterFactory.get_formatter('__no_existing__')
        assert isinstance(formatter, ConsoleFormatter)

    def test_console_formatter(self):
        start = Station('EW12', 'test1')
        end = Station('CC21', 'test3')
        formatter = ConsoleFormatter()
        response = formatter.format_routes(start, end, [])
        assert response == 'No available route find between {} and {}'.format(
            start, end
        )
        response = formatter.format_routes(
            start, end, [
                ([
                    start,
                    Station('TE1', 'test1'),
                    Station('TE2', 'test2'),
                    Station('CC22', 'test2'),
                    end,
                ], 5),
            ]
        ).split('\n')
        assert len(response) == 8
        assert response[0] == 'Recommended routes between {} and {}'.format(
            start, end
        )
        assert response[1] == 'Transfer to TE line'
        assert response[2] == (
            'Take TE line from Station[TE1,test1] to Station[TE2,test2]'
        )
        assert response[3] == (
            'Transfer to CC line'
        )
        assert response[4] == (
            'Take CC line from Station[CC22,test2] to Station[CC21,test3]'
        )
        response = formatter.format_routes(
            start, end, [
                ([
                    start,
                    Station('TE1', 'test1'),
                    Station('TE2', 'test2'),
                    Station('CC22', 'test2'),
                    end,
                ], 15),
            ],
            simple=False,
            limit=2,
        ).split('\n')
        assert len(response) == 9
        assert response[0] == 'Recommended routes between {} and {}'.format(
            start, end
        )
        assert response[1] == 'The estimated time: 15 mins'
        assert response[2] == 'Transfer to TE line'
        assert response[3] == (
            'Take TE line from Station[TE1,test1] to Station[TE2,test2]'
        )
        assert response[4] == (
            'Transfer to CC line'
        )
        assert response[5] == (
            'Take CC line from Station[CC22,test2] to Station[CC21,test3]'
        )
