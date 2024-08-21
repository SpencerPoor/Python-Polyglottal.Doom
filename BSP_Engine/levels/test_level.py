from settings import *

# POINTS x, y

# Level boundary walls
P_00 = (1.0, 1.0)
P_01 = (7.0, 1.0)
P_02 = (7.0, 8.0)
P_03 = (1.0, 8.0)
# Inner square pillar
P_04 = (3.0, 3.0)
P_05 = (3.0, 6.0)
P_06 = (6.0, 6.0)
P_07 = (6.0, 3.0)

SEGMENTS = [
    (P_00, P_01), (P_01, P_02), (P_02, P_03), (P_03, P_00),
    (P_04, P_05), (P_05, P_06), (P_06, P_07), (P_07, P_04),
]