from settings import *

class MapRenderer:
    # Rendering component to render geometry
    def __init__(self, engine):
        self.engine = engine
        self.camera = engine.camera

        # Obtains segments from level_data and stores them in raw_segments for use in MapRenderer
        raw_segments = [seg.pos for seg in self.engine.level_data.raw_segments]

        # Gets boundary points of the map by obtaining the farthest possible points available from raw_segments
        self.x_min, self.y_min, self.x_max, self.y_max = self.get_bounds(raw_segments)
        # Takes these points and redefines the raw_segments to accomodate the defined resolution-
        # -of the program (MAP_OFFSET, WIN_RES) via the remap_ methods used by remap_array further down in the code
        self.raw_segments = self.remap_array(raw_segments)

        # Creates remapped array of segments obtained during the creation of the BSP tree
        self.segments = self.remap_array(
            [seg.pos for seg in self.engine.bsp_builder.segments])
        # For animation, defines a counter
        self.counter = 0.0
        #
        self.is_draw_map = False

    def draw(self):
        # Callback to execute the drawing of the line segments from raw_segments, then the traversed BSP tree segments, then the drawing of the player
        self.draw_raw_segments()
        self.draw_segments()
        self.draw_player()
        self.counter += 0.0005

    def draw_player(self, dist = 100):
        # Draws player in the space
        x0, y0 = p0 = self.remap_vec2(self.engine.bsp_traverser.pos_2d)
        x1, y1 = p0 + self.camera.forward.xz * dist
        #
        ray.draw_line_v((x0, y0), (x1, y1), ray.WHITE)
        ray.draw_circle_v((x0, y0), 10, ray.GREEN)

    def draw_segments(self, seg_color=ray.ORANGE):
        # Draws the segments obtained during tree traversal (relative to camera position)
        segment_ids = self.engine.bsp_traverser.seg_ids_to_draw

        # Acquires position information from remapped list of segments via ID
        # for seg_id in segment_ids[:int(self.counter) % (len(segment_ids) + 1)]:
            # ^ Above was used to demonstrate drawing order of segments for purposes of understanding BSP tree traversal, but now no longer needed
        for seg_id in segment_ids:
            (x0, y0), (x1, y1) = p0, p1 = self.segments[seg_id]
            # Draws lines and normals to show front facing direction
            ray.draw_line_v((x0, y0), (x1, y1), seg_color)
            self.draw_normal(p0, p1, seg_color)
            # Draws segment points
            ray.draw_circle_v((x0, y0), 3, ray.WHITE)

    def draw_normal(self, p0, p1, color, scale=12):
        # Draws a line on a segment that signifies the front side of the segment
        # (important for visually defining the "front" and "back" of a line segment in relation to their defined places inside each segment on a Binary Space Partioning tree)
        # (See data_types file for more detail on Binary Space Partitioning)
        p10 = p1 - p0
        normal = normalize(vec2(-p10.y, p10.x))
        n0 = (p0 + p1) * 0.5
        n1 = n0 + normal * scale
        #
        ray.draw_line_v((n0.x, n0.y), (n1.x, n1.y), color)

    def draw_raw_segments(self):
        # Draws the actual lines in the rendering engine, connecting lines are visualized-
        # -with an ORANGE color provided by RayLib, points visualized with WHITE color
        for p0, p1 in self.raw_segments:
            (x0, y0), (x1, y1) = p0, p1
            ray.draw_line_v((x0, y0), (x1, y1), ray.DARKGRAY)

    # remap_ methods transform the defined boundaries from get_bounds to accomodate the defined resolution and offsets from settings (MAP_OFFSET, WIN_RES)
    def remap_array(self, arr: list[vec2]):

        return [(self.remap_vec2(p0), self.remap_vec2(p1)) for p0, p1 in arr]

    def remap_vec2(self, p: vec2):
        x = self.remap_x(p.x)
        y = self.remap_y(p.y)
        return vec2(x, y)

    def remap_x(self, x, out_min=MAP_OFFSET, out_max=MAP_WIDTH):
        return (x - self.x_min) * (out_max - out_min) / (self.x_max - self.x_min) + out_min
    
    def remap_y(self, y, out_min=MAP_OFFSET, out_max=MAP_HEIGHT):
        return (y - self.y_min) * (out_max - out_min) / (self.y_max - self.y_min) + out_min

    @staticmethod
    def get_bounds(segments: list[tuple[vec2]]):
        # Mathematical calculation that loops through all available segment points and determines, via comparing each point-
        # -against each other, which points are the farthest points out on the map in a 2D space, then defining the farthest-
        # -points as their own variables (x_min, x_max, y_min, y_max) and using them to define the map boundaries
        inf = float('inf')
        x_min, y_min, x_max, y_max = inf, inf, -inf, -inf
        #
        for p0, p1 in segments:
            x_min = p0.x if p0.x < x_min else p1.x if p1.x < x_min else x_min
            x_max = p0.x if p0.x > x_max else p1.x if p1.x > x_max else x_max
            #
            y_min = p0.y if p0.y < y_min else p1.y if p1.y < y_min else y_min
            y_max = p0.y if p0.y > y_max else p1.y if p1.y > y_max else y_max
        return x_min, y_min, x_max, y_max