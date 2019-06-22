MRT GUIDE
===============================================

Guide you through Singapore MRT systems.

### Requirements

Given a starting station and an ending station, find routes in the MRT system.
For more details, see [Problem description](./problem.md)

### Installation

For running the command line app, Python 3.6.8 is tested to work. Generally Python 3.4+ versions should work with no issues though.

0. Make sure Python 3.4+ is installed. If you do not have [pyenv](https://github.com/pyenv/pyenv), you can try pyenv for managing different versions of Python + virtualenv for project level Python version and library verion independence. Please refer to detailed instruction listed for pyenv or the system package manager for your OS.
1. The main app and package do not require additional package. For testing, please run `pip install -r requirements.txt` to install pytest and its extensions.

### Running instruction

For command line app, simply navigate to project root folder and run `python cmd_app.py`. Then you can type start station, end station and optionally the datetime representation. For example:

~~~
# input stations without datetime
Input start, end and optional datetime separated by comma or exit with "exit"/"e": Boon Lay,Little India
# output omitted
# input stations with datetime
Input start, end and optional datetime separated by comma or exit with "exit"/"e": Boon Lay,Little India,2019-01-31T18:00
# output omitted
# you can also use Station Code instead of Station Name
Input start, end and optional datetime separated by comma or exit with "exit"/"e": EW27,NE7
# output omitted
# or mixing Station Code and Station Name
Input start, end and optional datetime separated by comma or exit with "exit"/"e": Boon Lay,NE7
# output omitted
# and finally use e or exit to exit the app
~~~

You can tweak some configuration by changing the content of mrt_guide.ini. For example, you can change the data path or increase max number of recommended routes.

### Tests

Test files are under tests directory. To run all the tests, simply `pytest` will do the magic. For more advanced option like run a particular test or run tests with coverage, refer the documentation of pytest please.

### Developer Guide

#### Top Level Structure

There are mrt_guide, which is the source code of the package; tests, which contains all the testing related code and data; data, which holds the default MRT map data; cmd_app.py, which is entry point for the command line app; mrt_guide.ini, which is the configuration file used by cmd_app.py.

#### Main Package

The main logic is under mrt_guide directory. Structure:

* exceptions.py: contains all the exceptions defined for the package
* formatter.py: contains formatter base class, default formatter implementation for command line app and a register function to register formatter extensions by others
* mrt_map.py: contains path finding logic
* path_finder.py: wraps MRTMap, StationsReader and Weights
* station.py: modelling of a station
* stations_reader.py: read input data file
* weights.py: representation of waiting time as Weights

#### The good parts

* The whole project structure is very easy to understand as different modules do different things well and can work together nicely.
* Many modules are built with great extensibility. For example, MRTMap does not assume anything about waiting time, and can nicely support customized Weights with focus just on graph related logic. Another example is the decoupling of routes and formatter -- formatter can be extended with ease and the output can be changed from string to JSON or xml without any modification to the system. Close to modification but open to extension.
* The whole package takes in more parameters like limit to find fewer or more candidate routes as desired.
* The whole package can be used to compute shortest path among a start and an end station for a given date[1] without just filtering at stations_reader.

1. currently the system assume the map is static but the map is evolving in time in fact
