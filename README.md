# GTFS Graph Search (Python)
Public transport route planner console application, based on GTFS data (tested with a dataset from Koleje Dolnośląskie).  
Purpose of this project was to learn about heuristic search algorithms and practice structuring code in Python.

## Features
- preprocessing GTFS files into graph edges (`prepare_data.py`)
- graph representation with custom `Node`, `Edge`, and `Graph` classes
- route search with:
  - Dijkstra (travel time)
  - A* (travel time heuristic)
  - A* variant for transfer minimization
  - A* combined (time + transfer penalty)
- date-based service filtering (`calendar.txt`, `calendar_dates.txt`)
- CLI input for start, destination, criterion, and departure time

## Python concepts used
- object-oriented programming (`class`, constructors, methods)
- type hints (`dict[str, Node]`, `set[Edge]`, etc.)
- data structures: dictionaries, sets, lists, priority queue (`heapq`)
- file handling and CSV parsing (`csv`, `pandas`)
- datetime parsing and filtering (`datetime`)
- modular project structure (separate files for graph, search, utils, data prep)

## Built With
- Python
- pandas
- standard library modules: `csv`, `datetime`, `heapq`, `time`, `math`

## Run
1. (Optional) Create and activate [virtual environment](https://docs.python.org/3/library/venv.html).
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Generate graph data:
   - `python prepare_data.py`
4. Start the app:
   - `python main.py`