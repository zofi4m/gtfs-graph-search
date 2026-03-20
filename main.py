import sys
from graph import Graph, seconds_to_time
from search import dijkstra, astar
# TODO: A* variants

GRAPH_PATH = './graph_data.csv'

ALGORITHMS = {
    'd': ('Dijkstra', dijkstra),
    'a': ('A*', astar)
}

def print_path(path: list):
    if not path:
        print("No connection found", file=sys.stderr)
        return
    for edge in path:
        print(edge)

def select_algorithm() -> tuple:
    options = ', '.join(f"'{k}' = {label}" for k, (label, _) in ALGORITHMS.items())
    print(f"Select algorithm: {options}")
    while True:
        choice = input("algorithm> ").strip().lower()
        if choice in ALGORITHMS:
            label, fn = ALGORITHMS[choice]
            print(f"Using {label}.")
            return fn
        print(f"Error: choose one of {list(ALGORITHMS.keys())}.", file=sys.stderr)

def run(graph: Graph):
    algorithm = select_algorithm()
    print("Format: start;destination;criterion(t/p);departure_time [HH:MM:SS]")
    print("Type 'exit' to quit")
    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            break

        if raw.lower() == 'exit':
            break
        if not raw:
            continue

        parts = raw.split(';')
        if len(parts) != 4:
            print("Error: exactly 4 fields separated by ';' are required.", file=sys.stderr)
            continue

        start, end, criterion, start_time = [p.strip() for p in parts]
        if criterion not in ('t', 'p'):
            print("Error: criterion must be 't' (travel time) or 'p' (transfers).", file=sys.stderr)
            continue

        if start not in graph.name_map:
            print(f"Error: unknown stop '{start}'.", file=sys.stderr)
            continue
        if end not in graph.name_map:
            print(f"Error: unknown stop '{end}'.", file=sys.stderr)
            continue

        if criterion == 't':
            path, elapsed, cost = algorithm(graph, start, end, start_time)
            travel_time = seconds_to_time(cost)
            print_path(path)
            print(f"Minimized criterion (travel time): {travel_time}", file=sys.stderr)
            print(f"Computation time: {elapsed:.4f}s", file=sys.stderr)

        elif criterion == 'p':
            # path, elapsed, cost = astar_transfers(graph, start, end, start_time)
            print("Criterion 'p' not yet implemented.", file=sys.stderr)
            continue

if __name__ == "__main__":
    
    print("Loading graph...", file=sys.stderr)
    graph = Graph.construct(GRAPH_PATH)
    print("Graph loaded.\n", file=sys.stderr)
    run(graph)

'''
Example inputs:
Brzeg; Borowa Oleśnicka; t; 06:51:00

'''