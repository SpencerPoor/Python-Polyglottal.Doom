from settings import *
from data_types import BSPNode
from utils import is_on_front

# This traverses the Binary Space Partitioning tree using the root node as the starting point and the updated list of segments from bsp_builder as a sort of map to traverse with
class BSPTreeTraverser:
    def __init__(self, engine):
        self.engine = engine
        self.root_node = engine.bsp_builder.root_node
        self.segments = engine.bsp_builder.segments

        # Temp
        self.cam_pos = vec2(6, 7)
        self.seg_ids_to_draw = []

    def update(self):
        # Updates drawn segments relative to the location of the camera in-game
        self.seg_ids_to_draw.clear()
        self.traverse(self.root_node) # Starts traversal at root node

    def traverse(self, node: BSPNode):
        # Traverses the BSP to find the segments that need to be drawn, relative to the camera's current location in relation to the splitter
        if node is None:
            return None
        
        on_front = is_on_front(self.cam_pos - node.splitter_p0, node.splitter_vec)

        # Traverses tree and adds segments that need to be drawn to the seg_ids_to_draw list
        # This is configured to only add segments that render in the front subspace (aka player's point of view)
        if on_front:
            # If in front of the splitter, renders front to back
            self.traverse(node.front)
            #
            self.seg_ids_to_draw.append(node.segment_id)
            #
            self.traverse(node.back)
        else:
            # If behind the splitter, traverses but does not render segments in the back subspace
            self.traverse(node.back)
            #
            self.traverse(node.front)