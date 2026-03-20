import time
import heapq
from graph import Graph
from prepare_data import time_to_seconds

def dijkstra(graph: Graph, start_stop_name: str, end_stop_name: str, start_time: str):
    algorithm_start = time.perf_counter()
    start_seconds = time_to_seconds(start_time)

    s_id = graph.name_map[start_stop_name]
    e_id = graph.name_map[end_stop_name]
    print(f"{s_id} {e_id}")
    
    # initialize distances
    distances = {s_id : start_seconds}

    previous = {}

    # store (distance, node_id) in queue for ordering by distance
    pqueue = [(start_seconds, s_id)]

    while pqueue:
        start_seconds, curr_id = heapq.heappop(pqueue)

        if start_seconds > distances.get(curr_id, float('inf')):
            continue

        node = graph.nodes[curr_id]
        for edge in node.adjacent_edges:
            if edge.departure_time < start_seconds:
                continue
            
            neighbour = edge.end_node
            neighbour_weight = edge.arrival_time

            if edge.arrival_time < distances.get(neighbour.stop_id, float('inf')):
                distances[neighbour.stop_id] = neighbour_weight
                previous[neighbour.stop_id] = edge
                heapq.heappush(pqueue, (neighbour_weight, neighbour.stop_id))

    path = []
    curr_id = e_id

    while curr_id in previous:
        edge = previous[curr_id]
        path.insert(0, edge)
        curr_id = edge.start_node.stop_id
        
    algorithm_end = time.perf_counter()
    return path, algorithm_end - algorithm_start, distances[e_id]

if __name__=="__main__":
    pass
    