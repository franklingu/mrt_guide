'''Simple command line app to enable path finding in MRT stations.
'''
import os
from configparser import ConfigParser

from mrt_guide.path_finder import PathFinder
from mrt_guide.formatter import FormatterFactory


class SimpleCommandLineApp:
    def __init__(self, data_path, limit):
        self.path_finder = PathFinder(data_path)
        self.formatter = FormatterFactory.get_formatter()
        self.limit = limit

    def run(self):
        instruction = (
            'Input start, end and optional datetime separated by comma or'
            ' exit with "exit"/"e": '
        )
        print('Welcome to MRT Guide')
        while True:
            user_input = input(instruction)
            if user_input == 'exit' or user_input == 'e':
                break
            tokens = [elem.strip() for elem in user_input.split(',')]
            try:
                if len(tokens) == 2:
                    print(self.find_routes(tokens[0], tokens[1]))
                elif len(tokens) == 3:
                    print(self.find_routes(tokens[0], tokens[1], tokens[2]))
                else:
                    raise ValueError('Unrecognizable input')
            except ValueError as e:
                print('Error: {}. Please try again.'.format(str(e)))
            except Exception as e:
                print(
                    (
                        'Unknown error: {}.'
                        ' Sorry for this and try again.'
                    ).format(str(e))
                )
        print('Thanks for using MRT Guide')

    def find_routes(self, start, end, dt=None):
        return self.formatter.format_routes(
            start,
            end,
            self.path_finder.find_routes(start, end, dt, limit=self.limit),
            dt is None,
            limit=self.limit,
        )


if __name__ == '__main__':
    config_path = './mrt_guide.ini'
    data_path = './data/StationMap.csv'
    limit = 1
    if os.path.exists(config_path):
        config = ConfigParser()
        config.read(config_path)
        data_path = config['mrt_guide'].get('data_path', data_path)
        limit = int(config['mrt_guide'].get(
            'limit_of_recommended_routes', limit
        ))
    app = SimpleCommandLineApp(data_path, limit)
    app.run()
