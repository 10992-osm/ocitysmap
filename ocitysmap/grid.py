
import math, logging
import map_canvas, utils

l = logging.getLogger('ocitysmap')

class GridDescriptor:
    def __init__(self, bbox, db):
        self.bbox = bbox
        height, width = bbox.spheric_sizes()

        # Compute number of squares, assumming a size of 500 meters
        # per square
        self.width_square_count  = width / 500
        self.height_square_count = height / 500

        # Compute the size in angles of the squares
        self.width_square_angle  = (abs(bbox.get_top_left()[1] -
                                        bbox.get_bottom_right()[1]) /
                                    self.width_square_count)
        self.height_square_angle = (abs(bbox.get_top_left()[0] -
                                        bbox.get_bottom_right()[0]) /
                                    self.height_square_count)

        # Compute the lists of longitudes and latitudes of the
        # horizontal and vertical lines delimiting the square
        self.vertical_lines   = [bbox.get_top_left()[1] +
                                 x * self.width_square_angle
                                 for x in xrange(0, int(math.ceil(self.width_square_count )) + 1)]
        self.horizontal_lines = [bbox.get_top_left()[0] -
                                 x * self.height_square_angle
                                 for x in xrange(0, int(math.ceil(self.height_square_count)) + 1)]

        # Compute the lists of labels
        self.vertical_labels   = [utils.gen_vertical_square_label(x)
                                  for x in xrange(0, int(math.ceil(self.width_square_count)))]
        self.horizontal_labels = [utils.gen_horizontal_square_label(x)
                                  for x in xrange(0, int(math.ceil(self.height_square_count)))]
        l.debug("vertical lines: %s" % self.vertical_lines)
        l.debug("horizontal lines: %s" % self.horizontal_lines)
        l.debug("vertical labels: %s" % self.vertical_labels)
        l.debug("horizontal labels: %s" % self.horizontal_labels)

    def generate_shape_file(self, filename, bbox):
        g = map_canvas.GridFile(bbox, filename)
        for v in self.vertical_lines:
            g.add_vert_line(v)
        for h in self.horizontal_lines:
            g.add_horiz_line(h)
        g.flush()
        return g
