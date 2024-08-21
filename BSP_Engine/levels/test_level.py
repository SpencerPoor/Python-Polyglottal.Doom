from settings import *
# Custom map data to define geometry for level (Points, line segments)

# Defined POINTS x, y

# Level boundary walls
P_00 = (1.0, 1.0)
P_01 = (7.0, 1.0)
P_02 = (7.0, 8.0)
P_03 = (1.0, 8.0)
# Inner diamond pillar
P_04 = (4.5, 3.0)
P_05 = (3.0, 4.5)
P_06 = (4.5, 6.0)
P_07 = (6.0, 4.5)
# Inner triangle pillar
P_08 = (2.0, 4.0)
P_09 = (1.5, 6.5)
P_10 = (2.5, 6.5)
# Inner pentagon pillar
P_11 = (2.75, 1.4)
P_12 = (2.5, 1.8)
P_13 = (2.6, 2.4)
P_14 = (2.9, 2.4)
P_15 = (3.0, 1.8)

SETTINGS = {
    'seed': 1268,
    'cam_pos': (12, CAM_HEIGHT, 12),
    'cam_target': (5, CAM_HEIGHT, 5)
}

# Line Segments made with predefined points
SEGMENTS = [
    (P_04, P_05), (P_05, P_06), (P_06, P_07), (P_07, P_04), # Map Boundary
    (P_00, P_01), (P_01, P_02), (P_02, P_03), (P_03, P_00), # Diamond Pillar
    (P_08, P_09), (P_09, P_10), (P_10, P_08), # Triangle Pillar
    (P_11, P_12), (P_12, P_13), (P_13, P_14), (P_14, P_15), (P_15, P_11), # Pentagon pillar
]