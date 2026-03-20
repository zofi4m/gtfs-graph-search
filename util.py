from graph import Node, Edge
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

def heuristic_transfers(edge1: Edge, edge2: Edge) -> float:
    return float(edge1.line == edge2.line)
    
