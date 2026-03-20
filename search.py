import time
import heapq
from graph import Graph, Node
from prepare_data import time_to_seconds
from util import heuristic_distance

def dijkstra(graph: Graph, start_stop_name: str, end_stop_name: str, start_time: str):
    algorithm_start = time.perf_counter()
    start_seconds = time_to_seconds(start_time)

    s_id = graph.name_map[start_stop_name]
    e_id = graph.name_map[end_stop_name]
    
    # initialize distances
    distances = {s_id : start_seconds}

    previous = {}

    # store (distance, node_id) in queue for ordering by distance
    pqueue = [(start_seconds, s_id)]

    while pqueue:
        curr_time, curr_id = heapq.heappop(pqueue)

        if curr_time > distances.get(curr_id, float('inf')):
            continue

        node = graph.nodes[curr_id]
        for edge in node.adjacent_edges:
            if edge.departure_time < curr_time:
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
    return path, algorithm_end - algorithm_start, distances[e_id] - start_seconds

def astar(graph: Graph, start_stop_name: str, end_stop_name: str, start_time: str):
    algorithm_start = time.perf_counter()
    start_seconds = time_to_seconds(start_time)

    s_id = graph.name_map[start_stop_name]
    e_id = graph.name_map[end_stop_name]

    start_node = graph.nodes[s_id]
    end_node = graph.nodes[e_id]
    
    # initialize distances

    start_h_cost = heuristic_distance(start_node, end_node)
    
    heuristic_costs = {s_id: start_h_cost}
    graph_costs = {s_id : start_seconds}
    
    open_list = [(heuristic_costs, s_id)]
    visited = set()

    previous = {}

    while(open_list):
        curr_h, curr_id = heapq.heappop(open_list)
        if curr_id in visited:
            continue
        if curr_id == e_id:
            break
        
        curr_node = graph.nodes[curr_id]
        visited.add(curr_id)

        for edge in curr_node.adjacent_edges:
            if edge.departure_time < graph_costs[curr_id]:
                continue

            next = edge.end_node
            next_cost = edge.arrival_time
            if next_cost < graph_costs.get(next.stop_id, float('inf')):
                graph_costs[next.stop_id] = next_cost
                next_h_cost = heuristic_distance(next, end_node)
                heuristic_costs[next.stop_id] = next_h_cost
                previous[next.stop_id] = edge
                heapq.heappush(open_list, (next_cost + next_h_cost, next.stop_id))

    path = []
    curr_id = e_id

    while curr_id in previous:
        edge = previous[curr_id]
        path.insert(0, edge)
        curr_id = edge.start_node.stop_id
        
    algorithm_end = time.perf_counter()
                                                # TODO: h + g ?
    return path, algorithm_end - algorithm_start, graph_costs[e_id] - start_seconds

if __name__=="__main__":
    pass
    