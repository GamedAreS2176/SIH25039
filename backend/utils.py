import h3
from typing import Tuple
import math

def generate_h3_index(latitude: float, longitude: float, resolution: int = 8) -> str:
    """Generate H3 index for given coordinates"""
    return h3.lat_lng_to_cell(latitude, longitude, resolution)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat/2) * math.sin(dlat/2) + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2) * math.sin(dlon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

def get_h3_neighbors(h3_index: str, k: int = 1) -> list:
    """Get H3 neighbors at distance k"""
    return h3.grid_disk(h3_index, k)

def get_h3_children(h3_index: str, resolution: int) -> list:
    """Get H3 children at higher resolution"""
    return h3.cell_to_children(h3_index, resolution)

def get_h3_parent(h3_index: str, resolution: int) -> str:
    """Get H3 parent at lower resolution"""
    return h3.cell_to_parent(h3_index, resolution)