import pandas as pd

DATASET_PATH = './data/'

def time_to_seconds(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

def prepare_data():
    # import ids as string, so that they dont get converted to float
    stops = pd.read_csv(DATASET_PATH + 'stops.txt', dtype={
        'stop_id': pd.StringDtype(),
        'stop_name': pd.StringDtype(),
        'parent_station': pd.StringDtype(),
    })
    stops = stops[['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'parent_station']]

    stop_times = pd.read_csv(DATASET_PATH + 'stop_times.txt', dtype={
        'trip_id': pd.StringDtype(),
        'stop_id': pd.StringDtype()
    })
    stop_times = stop_times[[
        'trip_id', 'stop_id', 'arrival_time', 'departure_time', 'stop_sequence'
    ]]

    routes = pd.read_csv(DATASET_PATH + 'routes.txt', dtype={
        'route_id': pd.StringDtype(),
    })
    routes = routes[['route_id', 'route_short_name', 'route_long_name']]

    trips = pd.read_csv(DATASET_PATH + 'trips.txt', dtype={
        'route_id': pd.StringDtype(),
        'trip_id': pd.StringDtype(),
        'service_id': pd.StringDtype()
    })
    trips = trips[['route_id', 'trip_id', 'service_id']]
    
    stop_times['departure_time'] = stop_times['departure_time'].apply(time_to_seconds)
    stop_times['arrival_time'] = stop_times['arrival_time'].apply(time_to_seconds)
    
    edges = pd.merge(stop_times, trips, on='trip_id')
    edges = pd.merge(edges, routes, on='route_id')
    edges = pd.merge(edges, stops, on='stop_id')

    edges = edges.sort_values(['trip_id', 'stop_sequence'])

    # determining arrival stop at each edge
    # by getting the next stop in stop_sequence
    next_stop = edges.shift(-1)
    edges['next_stop_id'] = next_stop['stop_id']
    edges['arrival_at_next'] = next_stop['arrival_time']
    edges['next_parent_station'] = next_stop['parent_station']
    edges['next_stop_name'] = next_stop['stop_name']
    edges['next_stop_lat'] = next_stop['stop_lat']
    edges['next_stop_lon'] = next_stop['stop_lon']

    # eliminate the last stop (does not have next stop)
    edges = edges[edges['trip_id'] == next_stop['trip_id']]

    cols_to_save = [
        'stop_id', 'next_stop_id', 'stop_name', 'next_stop_name', 'departure_time', 'arrival_at_next', 'parent_station', 
        'next_parent_station', 'route_short_name', 'route_long_name', 'trip_id', 
        'service_id', 'stop_lat', 'stop_lon', 'next_stop_lat', 'next_stop_lon', 'stop_sequence'
    ]
    edges[cols_to_save].to_csv('graph_data.csv', index=False)

if __name__ == '__main__':
    prepare_data()