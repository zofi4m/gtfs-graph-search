import time
import heapq
from graph import Graph, Node
from prepare_data import time_to_seconds
from util import heuristic_distance, get_contour_map, cost_transfers, TRANSFER_WEIGHT

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

    if e_id not in distances:
        return [], algorithm_end - algorithm_start, float('inf')

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
    
    open_list = [(start_seconds + start_h_cost, s_id)]
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

    if e_id not in graph_costs:
        return [], algorithm_end - algorithm_start, float('inf')
                                                
    return path, algorithm_end - algorithm_start, graph_costs[e_id] - start_seconds

def astar_transfers(graph: Graph, start_stop_name: str, end_stop_name: str, start_time: str):
    algorithm_start = time.perf_counter()
    start_seconds = time_to_seconds(start_time)

    s_id = graph.name_map[start_stop_name]
    e_id = graph.name_map[end_stop_name]

    end_node = graph.nodes[e_id]
    
    contour_map = get_contour_map(graph, end_node)
    graph_costs = {s_id : 0}
    # for tracking chronology
    arrivals = {s_id: start_seconds}

    open_list = [(contour_map.get(s_id, 0), 0, s_id)]
    visited = set()

    previous = {}

    while(open_list):
        curr_h, curr_t, curr_id = heapq.heappop(open_list)
        if curr_id in visited:
            continue
        if curr_id == e_id:
            break
        
        curr_node = graph.nodes[curr_id]
        visited.add(curr_id)
        prev_edge = previous.get(curr_id)
        

        for edge in curr_node.adjacent_edges:
            if edge.departure_time < arrivals[curr_id]:
                continue

            transfer = cost_transfers(prev_edge, edge) if prev_edge else 0
            new_transfers = graph_costs[curr_id] + transfer

            next = edge.end_node
            next_id = next.stop_id
            curr_best_transfers = graph_costs.get(next_id, float('inf'))
            curr_best_arrival = arrivals.get(next_id, float('inf'))
            # ensure not dropping equally good transfers with better time
            if (new_transfers < curr_best_transfers or
                    (new_transfers == curr_best_transfers and edge.arrival_time < curr_best_arrival)):
                previous[next_id] = edge
                graph_costs[next_id] = new_transfers
                arrivals[next_id] = edge.arrival_time
                h = contour_map.get(next_id, 0)
                                                        # arrival time for breaking ties
                heapq.heappush(open_list, (new_transfers + h, edge.arrival_time, next_id))

    path = []
    curr_id = e_id

    while curr_id in previous:
        edge = previous[curr_id]
        path.insert(0, edge)
        curr_id = edge.start_node.stop_id
        
    algorithm_end = time.perf_counter()
    return path, algorithm_end - algorithm_start, graph_costs.get(e_id, 0)

def astar_combined(graph: Graph, start_stop_name: str, end_stop_name: str, start_time: str):
    algorithm_start = time.perf_counter()
    start_seconds = time_to_seconds(start_time)

    s_id = graph.name_map[start_stop_name]
    e_id = graph.name_map[end_stop_name]

    start_node = graph.nodes[s_id]
    end_node = graph.nodes[e_id]
    
    start_h_cost = heuristic_distance(start_node, end_node)
    
    arrivals = {s_id : 0}
    penalties = {s_id : 0}
    
    open_list = [(start_h_cost, start_seconds, s_id)]
    visited = set()

    previous = {}

    while(open_list):
        curr_f, curr_t, curr_id = heapq.heappop(open_list)
        if curr_id in visited:
            continue
        if curr_id == e_id:
            break

        curr_node = graph.nodes[curr_id]
        visited.add(curr_id)
        prev_edge = previous.get(curr_id)
        
        for edge in curr_node.adjacent_edges:
            if edge.departure_time < curr_t:
                continue

            next = edge.end_node
            next_id = next.stop_id
            penalty = TRANSFER_WEIGHT if (prev_edge and prev_edge.trip != edge.trip) else 0
            new_penalty = penalties[curr_id] + penalty
            combined = edge.arrival_time + new_penalty

            if combined < arrivals.get(next_id, float('inf')) + penalties.get(next_id, 0):
                penalties[next_id] = new_penalty
                arrivals[next_id] = edge.arrival_time
                previous[next_id] = edge
                h = heuristic_distance(edge.end_node, end_node)
                heapq.heappush(open_list, (combined + h, edge.arrival_time, next_id))

    path = []
    curr_id = e_id

    while curr_id in previous:
        edge = previous[curr_id]
        path.insert(0, edge)
        curr_id = edge.start_node.stop_id
        
    algorithm_end = time.perf_counter()
    
    if e_id not in arrivals:
        return [], algorithm_end - algorithm_start, 0, float('inf')
    
    n_transfers = sum(cost_transfers(a, b) for a, b in zip(path, path[1:]))
    travel_time = path[-1].arrival_time - start_seconds if path else 0
    return path, algorithm_end - algorithm_start, n_transfers, travel_time

    