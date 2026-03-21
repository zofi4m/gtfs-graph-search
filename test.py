from graph import Graph, get_services_for_date, seconds_to_time
import datetime as dt
from search import *

def test_graph1():
    graph = Graph.construct('./graph_data.csv')
    for n in graph.nodes.values():
        print(n.name)

    stop_id = graph.name_map['Wrocław Psie Pole']
    node = graph.nodes[stop_id]
    for edge in node.adjacent_edges:
        print(edge)

def test_graph2():
    graph = Graph.construct('./graph_data.csv')
    for n in graph.nodes.values():
        print(n)
    node = graph.nodes['1413085']
    for e in node.adjacent_edges:
        print(e)

def test_graph3():
    graph = Graph.construct('./graph_data.csv')
    node = graph.nodes[graph.name_map['Trzebnica']]
    for edge in node.adjacent_edges:
        print(f"{edge.start_node.name} -> {edge.end_node.name} dep:{seconds_to_time(edge.departure_time)}")

def test_date_filter1():
    print(dt.datetime.strptime('20260601', '%Y%m%d'))
    print(dt.datetime.strptime('20260601', '%Y%m%d').weekday())
    services = get_services_for_date('20260601')
    print(services)

    print("Mon:", len(get_services_for_date('20260615')))
    print("Sat:", len(get_services_for_date('20260620')))
    print("Sun:", len(get_services_for_date('20260621')))

def test_date_filter2():
    services = get_services_for_date('20260303')
    print("services:", list(services)[:10])

def test_dijkstra1():
    graph = Graph.construct('./graph_data.csv')
    path, t, crit = dijkstra(graph, 'Rawicz', 'Wrocław Główny', '13:33:00')
    for e in path:
        print(e)
    print(t, crit, sep=' ')

    path2, t2, crit2 = dijkstra(graph, 'Brzeg', 'Borowa Oleśnicka', '4:34:04')
    for e in path2:
        print(e)
    print(t2, crit2, sep=' ')

# import pandas as pd
# df = pd.read_csv('graph_data.csv', dtype={
#     'stop_id': pd.StringDtype(),
#     'parent_station': pd.StringDtype(),
#     'next_parent_station': pd.StringDtype(),
# })

# mask = (df['stop_name'] == 'Trzebnica') & (df['next_stop_name'] == 'Wrocław Zakrzów')
# print(df[mask][['trip_id', 'stop_name', 'next_stop_name', 'stop_sequence']])

