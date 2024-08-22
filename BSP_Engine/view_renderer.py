from settings import *
from models import Models

# Creates instance of Models class and renders it into the program
class ViewRenderer:
    def __init__(self, engine):
        self.engine = engine
        #
        self.segments = engine.bsp_builder.segments
        self.camera = engine.camera
        self.segment_ids_to_draw = self.engine.bsp_traverser.seg_ids_to_draw
        #
        self.models = Models(engine)
        self.wall_models = self.models.wall_models
        #
        # "set is used to remove duplicate indexes in case segments refer to the same model for the raw segment"
        self.wall_ids_to_draw = set()
        #
        self.screen_tint = WHITE_COLOR

    def update(self):
        self.wall_ids_to_draw.clear()

        # Iterates through the list of segments obtained when traversing the BSP tree
        for seg_id in self.segment_ids_to_draw:
            # Walls
            seg = self.segments[seg_id]
            # Forms a set of wall model indexes, rendered in below draw method
            self.wall_ids_to_draw |= seg.wall_model_id

    def draw(self):
        # Draws walls
        for wall_id in self.wall_ids_to_draw:
            ray.draw_model(self.wall_models[wall_id], VEC3_ZERO, 1.0, self.screen_tint)

    def update_screen_tint(self):
        self.screen_tint = (
            DARK_GRAY_COLOR if self.engine.map_renderer.is_draw_map else WHITE_COLOR
        )