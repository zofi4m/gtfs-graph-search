from graph import Graph

graph = Graph.construct('./graph_data.csv')
for n in graph.nodes.values():
    print(n.name)

stop_id = graph.name_map['Wrocław Psie Pole']
node = graph.nodes[stop_id]
for edge in node.adjacent_edges:
    print(edge)