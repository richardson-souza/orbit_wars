import json
import math
from core.physics import point_to_segment_distance

def check_collision():
    p12 = (54.4405, 83.0677)
    p18_pred = (68.8818, 84.6258)
    p20 = (65.23, 83.13)
    
    dist = point_to_segment_distance(p20, p12, p18_pred)
    print(f"Distance from Planet 20 to the trajectory line from Planet 12 to Planet 18: {dist:.4f}")
    print(f"Planet 20 radius: 2.1")
    print(f"Does it collide? {'YES' if dist < 2.1 else 'NO'}")

check_collision()
