import csv, datetime as dt

class Node:
    def __init__(self, stop_id: str, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.adjacent_edges: set[Edge] = set()
        self.stop_id = stop_id

    def add_edge(self, edge):
        self.adjacent_edges.add(edge)

    def __str__(self):
        return f"{self.stop_id} {self.name} lat:{self.latitude} lon:{self.longitude}"

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
        return f"Route {self.route}: {self.start_node.name}:{seconds_to_time(self.departure_time)} -> {self.end_node.name}:{seconds_to_time(self.arrival_time)}"

class Graph:
    '''
        Nodes are stored in a dictionary stop_id: node (for edge grouping by parent station).
        Edges are stored as adjacent edges in Node.
    '''
    def __init__(self, nodes, name_map, incoming_edges):
        self.nodes = nodes
        self.name_map = name_map
        self.incoming_edges = incoming_edges
                                       # friday 
    def construct(file_path: str, date='20260324'):
        '''
        Default date: 24.03.2026
        '''
        nodes : dict[str, Node] = dict()
        name_map : dict[str, str] = dict()
        incoming_edges : dict[str, list[Edge]] = dict()
        active_services = get_services_for_date(date)
        with open(file_path, mode='r', encoding='utf-8') as graph_file:
            reader = csv.DictReader(graph_file)
            for row in reader:
                s_id = row['parent_station'] if row['parent_station'] else row['stop_id']
                e_id = row['next_parent_station'] if row['next_parent_station'] else row['next_stop_id']

                if s_id not in nodes:
                    nodes[s_id] = Node(s_id, row['stop_name'], float(row['stop_lat']), float(row['stop_lon']))
                start_node = nodes[s_id]

                if e_id not in nodes:
                    nodes[e_id] = Node(e_id, row['next_stop_name'], float(row['next_stop_lat']), float(row['next_stop_lon']))
                end_node = nodes[e_id]

                if row['service_id'] not in active_services:
                    continue
                
                # collapse route names
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
                if e_id not in incoming_edges:
                    incoming_edges[e_id] = []
                incoming_edges[e_id].append(new_edge)

        return Graph(nodes=nodes, name_map=name_map, incoming_edges=incoming_edges)
    
def get_services_for_date(date: str) -> set[str]:
    DATASET_PATH = './data/'
    DATE_FORMAT = '%Y%m%d'

    services = set()
    curr_date = dt.datetime.strptime(date, DATE_FORMAT)

    # map weekday number to name
    days = [
        'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday'
    ]
    day_col = days[curr_date.weekday()]

    ######### calendar.txt ##########
    with open(DATASET_PATH + 'calendar.txt') as calendar:
        reader = csv.DictReader(calendar)
        for row in reader:
            s_id = row['service_id']
            start_date = dt.datetime.strptime(row['start_date'], DATE_FORMAT)
            end_date = dt.datetime.strptime(row['end_date'], DATE_FORMAT)

            if start_date <= curr_date <= end_date:
                if row[day_col] == '1':
                    services.add(s_id)
                
    ######### calendar_dates.txt ##########
    with open(DATASET_PATH + 'calendar_dates.txt') as dates:
        reader = csv.DictReader(dates)
        for row in reader:
            s_id = row['service_id']
            except_date = dt.datetime.strptime(row['date'], DATE_FORMAT)
            except_type = row['exception_type']

            if except_date == curr_date:
                if except_type == '1':
                    services.add(s_id)
                elif except_type == '2':
                    services.discard(s_id)
    return services

def seconds_to_time(s):
    s = int(s)
    return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"