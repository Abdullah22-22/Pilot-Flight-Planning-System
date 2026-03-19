import math

def calc_distance(lat1, lon1, lat2, lon2):

    R = 6371  

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


WORLD_MAP = {
    "width": 1200,
    "height": 600,
    "lon_min": -180,
    "lon_max": 180,
    "lat_min": -90,
    "lat_max": 90
}
