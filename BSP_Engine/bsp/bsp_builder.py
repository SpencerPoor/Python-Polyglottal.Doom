from settings import *
from data_types import Segment, BSPNode
from utils import cross_2d
from copy import copy
import random

# Builds the Binary Space Partitioning tree using the BSPNode class template found in data_types
class BSPTreeBuilder:
    def __init__(self, engine):
        self.engine = engine
        self.raw_segments = engine.level_data.raw_segments
        # Defines the root node of the BSP tree to start the partitioning process from
        self.root_node = BSPNode()
        # New segment list of segments created during the creation of the BSP tree
        self.segments = []
        self.seg_id = 0
        
        # This acquires the best possible order in which to generate the BSP tree with the least amount of splits, improving performance
        # THIS MUST BE RUN AHEAD OF TIME AFTER THE FINAL LEVEL GEOMETRY DATA HAS BEEN FINALIZED
            # seed = self.find_best_seed()

        # After best seed has been calculated and found ahead of time via the find_best_seed method, the resulting seed can be set as the seed that will be used when running the program
        seed = self.engine.level_data.settings['seed']
        random.seed(seed)
        random.shuffle(self.raw_segments)

        self.num_front, self.num_back, self.num_splits = 0, 0, 0

        # Method that will build the tree using the respective method further down in this class
        self.build_bsp_tree(self.root_node, self.raw_segments)
        #
        print('num_front:', self.num_front)
        print('num_back:', self.num_back)
        print('num_splits:', self.num_splits)

    def find_best_seed(self, start_seed=0, end_seed=20_000, weight_factor=3):
        # Function that checks within provided range of seeds that dictate the order in which BSP is constructed (20,000) and finds the random seed with the most optimal tree construction order
        best_seed, best_score = -1, float('inf')
        # Loops through each seed in range, finds an optimal seed with a low number of splits
        for seed in range(start_seed, end_seed):
            raw_segments = self.raw_segments.copy()
            random.seed(seed)
            random.shuffle(raw_segments)
            #
            root_node = BSPNode()
            self.segments = []
            self.seg_id = 0
            #
            self.num_front, self.num_back, self.num_splits = 0, 0, 0
            self.build_bsp_tree(root_node, raw_segments)
            # Score determines how optimal the seed is, lower is better
            score = abs(self.num_back - self.num_front) + weight_factor * self.num_splits
            if score < best_score:
                best_seed, best_score = seed, score

        print('best_seed =', best_seed, 'score = ', best_score)
        # Gives the best seed to use
        return best_seed

    def split_space(self, node: BSPNode, input_segments: list[Segment]):
        # Splitter segment will always be the first segment in the list of segments available
        splitter_seg = input_segments[0]

        splitter_pos = splitter_seg.pos
        splitter_vec = splitter_seg.vector

        # Assign attributes of segment that will be splitter (vector, coordinate points) to the current node in the BSP tree
        node.splitter_vec = splitter_vec
        node.splitter_p0 = splitter_pos[0]
        node.splitter_p1 = splitter_pos[1]

        front_segs, back_segs = [], []

        # VERY COMPLICATED MATH to determine how to split segments into their respective front and back spaces
        # I will likely never fully understand how the math works and therefore this part I will likely never be able to fully explain,
        # -but I can understand what it does and what it accomplishes for splitting the space and assigning segments to respective front and back sections
        for segment in input_segments[1:]:
            #
            segment_start = segment.pos[0]
            segment_end = segment.pos[1]
            segment_vector = segment.vector
            #
            numerator = cross_2d((segment_start - splitter_pos[0]), splitter_vec)
            denominator = cross_2d(splitter_vec, segment_vector)

            # if the denominator is zero the lines are parallel
            denominator_is_zero = abs(denominator) < 1e-4
            # segments are collinear if they are parallel and the numerator is zero
            numerator_is_zero = abs(numerator) < 1e-4
            #
            if denominator_is_zero and numerator_is_zero:
                front_segs.append(segment)
                continue
            if not denominator_is_zero:
                # intersection is the point on a line segment where the line divides it
                intersection = numerator / denominator

                # segments that are not parallel and t is in (0,1) should be divided
                if 0.0 < intersection < 1.0:
                    self.num_splits += 1
                    #
                    intersection_point = segment_start + intersection * segment_vector

                    r_segment = copy(segment)
                    r_segment.pos = segment_start, intersection_point
                    r_segment.vector = r_segment.pos[1] - r_segment.pos[0]
                    #
                    l_segment = copy(segment)
                    l_segment.pos = intersection_point, segment_end
                    l_segment.vector = l_segment.pos[1] - l_segment.pos[0]

                    if numerator > 0:
                        l_segment, r_segment = r_segment, l_segment
                    #
                    front_segs.append(r_segment)
                    back_segs.append(l_segment)
                    continue
            if numerator < 0 or (numerator_is_zero and denominator > 0):
                front_segs.append(segment)
            #
            elif numerator > 0 or (numerator_is_zero and denominator < 0):
                back_segs.append(segment)

        # Adds all segments, in particular newly created ones from segment splits, to a new segment list to track all segments that exist after the BSP tree is created
        self.add_segment(splitter_seg, node)
        return front_segs, back_segs
    
    def add_segment(self, splitter_seg: Segment, node: BSPNode):
        self.segments.append(splitter_seg)
        node.segment_id = self.seg_id
        #
        self.seg_id += 1

    def build_bsp_tree(self, node: BSPNode, input_segments: list[Segment]):
        # If there are no line segments, exists function
        if not input_segments:
            return None
        
        # Defines back and front segments that are acquired from split_space function
        front_segs, back_segs = self.split_space(node, input_segments)

        # Recursively calls function to create further child nodes using front and back segments available
        if back_segs:
            self.num_back += 1
            #
            node.back = BSPNode()
            self.build_bsp_tree(node.back, back_segs)

        if front_segs:
            self.num_front += 1
            #
            node.front = BSPNode()
            self.build_bsp_tree(node.front, front_segs)