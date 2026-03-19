from graph import Graph, Node, get_services_for_date
import datetime as dt

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
    node = graph.nodes['1413085.0']
    for e in node.adjacent_edges:
        print(e)

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

# TODO: test graph + filtr

test_graph2()