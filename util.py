from graph import Node, Edge, Graph
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6_371_000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    hav = sin(dphi / 2)**2 + cos(phi1) * cos(phi2) * sin(dlambda / 2)**2
    
    return R * 2 * atan2(sqrt(hav), sqrt(1-hav))

# KD max speed: 160 km/h
MAX_SPEED_MS = 200_000 / 3600

def heuristic_distance(node: Node, end: Node) -> float:
    dist = haversine(node.latitude, node.longitude,
                     end.latitude, end.longitude)
    return dist / MAX_SPEED_MS

def cost_transfers(edge1: Edge, edge2: Edge) -> float:
    return 0 if edge1.route == edge2.route else 1

def get_contour_map(graph: Graph, dest: Node) -> dict:
    '''
    Returns dictionary with mapping: {stop_id: manhattan distance from goal}
    '''
    d_id = dest.stop_id
    contour = {d_id: 0}
    queue = [d_id]
    
    while (queue):
        curr_id = queue.pop(0)
        curr_transfers = contour[curr_id]
        incoming_edges = graph.incoming_edges[curr_id]
        for edge in incoming_edges:
            next_id = edge.start_node.stop_id
            if next_id not in contour:
                contour[next_id] = curr_transfers + 1
                queue.append(next_id)

    return contour


    
