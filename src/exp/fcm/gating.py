import numpy as np

def is_inside_convex_polygon(point, polygon):
    x, y = point
    inside = True
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1) % len(polygon)]
        # 外積を計算して向きを判定
        cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if cross < 0:  # 一つでも外側ならアウト
            inside = False
            break
    return inside
