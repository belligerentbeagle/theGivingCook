from shapely.geometry import Point, mapping


def create_geojson_circle(center, radius_km):
    center_point = Point(center[1], center[0])
    circle = center_point.buffer(radius_km / 111.12)
    return mapping(circle)


def calculate_zoom_level(max_distance):
    print(f"max dist {max_distance}")
    if max_distance <= 1:
        return 13.2
    elif max_distance <= 3:
        return 13
    elif max_distance <= 5:
        return 12
    elif max_distance <= 7:
        return 11.5
    elif max_distance <= 10:
        return 10.8
    elif max_distance <= 15:
        return 10.5
    elif max_distance <= 20:
        return 10
    else:
        return 9
