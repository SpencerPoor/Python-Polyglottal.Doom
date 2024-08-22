from settings import *
# Custom map data to define geometry for level (Points, line segments)

# Defined POINTS x, y

# points
P_00 = (1.0, 1.0)
P_01 = (14.0, 1.0)
P_02 = (14.0, 16.0)
P_03 = (1.0, 16.0)
#
P_04 = (11.0, 4.0)
P_05 = (9.0, 8.0)
P_06 = (11.0, 12.0)
P_07 = (13.0, 8.0)
#
P_08 = (3.6, 3.6)
P_09 = (3.6, 8.4)
P_10 = (7.0, 8.4)
P_11 = (7.0, 3.6)
#
P_12 = (3.0, 11.0)
P_13 = (3.0, 13.0)
P_14 = (4.0, 13.0)
P_15 = (4.0, 11.0)
#
P_16 = (7.6, 9.6)
P_17 = (5.4, 14.2)
P_18 = (9.6, 14.2)

SETTINGS = {
    'seed': 4178,
    'cam_pos': (13, CAM_HEIGHT, 13),
    'cam_target': (5, CAM_HEIGHT, 5)
}

# Line Segments made with predefined points
SEGMENTS = [
    (P_04, P_05), (P_05, P_06), (P_06, P_07), (P_07, P_04),
    (P_00, P_01), (P_01, P_02), (P_02, P_03), (P_03, P_00),
    (P_08, P_09), (P_09, P_10), (P_10, P_11), (P_11, P_08),
    (P_12, P_13), (P_13, P_14), (P_14, P_15), (P_15, P_12),
    (P_16, P_17), (P_17, P_18), (P_18, P_16),
]