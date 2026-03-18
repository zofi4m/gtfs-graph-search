import csv, datetime as dt

class Node:
    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.adjacent_edges: set[Edge] = set()

    def add_edge(self, edge):
        self.adjacent_edges.add(edge)

    def __str__(self):
        return f"{self.name}"

class Edge:
    def __init__(self, route: str, service: str, start_node: Node, end_node: Node, 
                 departure_time: float, arrival_time: float):
        self.route = route
        self.start_node = start_node
        self.end_node = end_node
        self.departure_time = departure_time # from start
        self.arrival_time = arrival_time # at end
        self.service = service

    def __str__(self):
        return f"Route {self.route}: {self.start_node.name}:{self.departure_time} -> {self.end_node.name}:{self.arrival_time}"

class Graph:
    '''
        Nodes are stored in a dictionary stop_id: node (for edge grouping by parent station).
        Edges are stored as adjacent edges in Node.
    '''
    def __init__(self, nodes, name_map):
        self.nodes = nodes
        self.name_map = name_map

    def construct(file_path: str, date='15-03-2026'):
        nodes : dict[str, Node] = dict()
        name_map : dict[str, str] = dict()
        '''
        TODO:
            - check service validity (date)
            - map names -> parent_id
        '''
        with open(file_path, mode='r', encoding='utf-8') as graph_file:
            reader = csv.DictReader(graph_file)
            for row in reader:
                s_id = row['parent_station'] if row['parent_station'] else row['stop_id']
                e_id = row['next_parent_station'] if row['next_parent_station'] else row['next_stop_id']

                if s_id not in nodes:
                    nodes[s_id] = Node(row['stop_name'], float(row['stop_lat']), float(row['stop_lon']))
                start_node = nodes[s_id]

                if e_id not in nodes:
                    nodes[e_id] = Node(row['next_stop_name'], float(row['next_stop_lat']), float(row['next_stop_lon']))
                end_node = nodes[e_id]

                # collapse route names?
                route_name = row['route_short_name'] if row['route_short_name'] else row['route_long_name']
                new_edge = Edge(
                    route=route_name,
                    service=row['service_id'],
                    start_node=start_node,
                    end_node=end_node,
                    departure_time=float(row['departure_time']),
                    arrival_time=float(row['arrival_at_next'])
                )
                start_node.add_edge(new_edge)

                name_map[row['stop_name']] = s_id
                name_map[row['next_stop_name']] = e_id

        return Graph(nodes=nodes, name_map=name_map)
    
def get_services_for_date(date: str) -> set[str]:
    DATASET_PATH = './data/'
    DATE_FORMAT = '%YYYY%MM%DD'

    services = set()
    curr_date = dt.strptime(date, DATE_FORMAT)
    with open(DATASET_PATH + 'calendar.txt') as calendar:
        reader = csv.DictReader(calendar)
        for row in reader:
            s_id = row['service_id']
            start_date = dt.strptime(row['start_date'], DATE_FORMAT)
            end_date = dt.strptime(row['start_date'], DATE_FORMAT)
            if (start_date <= curr_date and curr_date >= end_date):
                services.add(s_id)

    with open(DATASET_PATH + 'calendar_dates.txt') as dates:
        reader = csv.DictReader(dates)
        for row in reader:
            s_id = row['service_id']