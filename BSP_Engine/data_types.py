from settings import *

# Define the parts of the geometry that form the virtual space
class Segment:
    # Creates a line segment defined by 2 points with coordinates on a 2D plane
    def __init__(self, p0: tuple[float], p1: tuple[float]):
        
        # Defines the coordinate points of a segment
        self.pos: tuple[vec2] = vec2(p0), vec2(p1)
        # Defines the magnitude (length) of a vector (line)
        self.vector: vec2 = self.pos[1] - self.pos[0]



# This class defines a node and its variables on a Binary Space Partitioning tree
# For the following explanations, please refer to the BSP_diagram file found in this project's VisualAidImages folder to visualize how the partitioning works
class BSPNode:
    def __init__(self):

        # Defines a "front" and "back" child node duo defined relative to the "splitter" (splitter is the segment line that "splits" the space in half)
            # The initial root line segment splits the rendered space into two subspaces, a front and back, which relegates the segments found in the front and back into their "front" and "back" subspaces respectively
            # The action of splitting is recursively repeated on all child nodes
                # For example, entering a child node in the back subspace, the child segment's node then splits that back subspace again into "front" and "back" subspaces as defined by its own splitter location, INSIDE of the initial back subspace, with remaining unassigned nodes put into those "front" and "back" subspaces again
                # Repeated until every individual segment node has its own assigned spot on the Binary Space Partitioning tree
            # In the event a line segment is in both of a segment's "front" and "back" subspaces, that line segment gets split into two new line segments, a line segment for the front space and one for the back space

        # "front" contains a child segment found in the "front" space of a segment node
        self.front: BSPNode = None
        # "back" contains a child segment found in the "front" space of a segment node
        self.back: BSPNode = None

        # Defines coordinates of the splitter's (segment's vector's) points to be used to calculate what subspace all following segments are located in
        self.splitter_p0: vec2 = None
        self.splitter_p1: vec2 = None
        self.splitter_vec: vec2 = None
        # Identify whether node is a splitter node via id
        self.segment_id: int = None