import numpy as np

class Roundabout():
    def __init__(self):
        self.exceptions = []
        self.queue = np.array(([]))
    
    # Gets all the indexes between 2 points in the matrix.
    def get_area(self, points):
        area = []

        # Each element in points is a tuple of 2 coordinates. Each coordinate is a tuple of its x and y value.s
        for point in points:
            x1, y1 = point[0]
            x2, y2 = point[1]
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    area.append((i,j))
        return area


class Regular(Roundabout):
    def __init__(self):
        self.size = 11
        self.points = [((3,3),(25,25))]
        self.area = self.get_area(self.points)
        self.grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 3, 0, 0, 0],
                              [0, 0, 0, 5, 3, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 3, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [2, 5, 5, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 8, 5, 5, 1],
                              [2, 5, 5, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 1],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [1, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 5, 5, 5, 2],
                              [1, 5, 5, 8, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 5, 5, 2],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 3, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 8, 5, 5, 5, 5, 5, 5, 5, 3, 5, 0, 0, 0],
                              [0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5, 5, 5, 3, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


class Turbo(Roundabout):
    def __init__(self):
        self.size = 11
        self.points = [((3,3),(25,25))]
        self.area = self.get_area(self.points)
        self.grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 7, 5, 5, 5, 5, 5, 5, 5, 3, 0, 0, 0],
                              [0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 3, 5, 0, 0, 0],
                              [0, 0, 0, 5, 3, 5, 5, 5, 5, 5, 5, 5, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [2, 5, 5, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 8, 5, 5, 1],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 1],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [1, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [1, 5, 5, 8, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6, 5, 5, 2],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 5, 5, 5, 5, 5, 5, 5, 3, 5, 0, 0, 0],
                              [0, 0, 0, 5, 3, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5, 5, 5, 3, 0, 0, 0],
                              [0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 7, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


class Magic(Roundabout):
    def __init__(self):
        self.size = 29
        self.points = [((3,11),(9,17)), ((11,19),(17,25)), ((19,11),(25,17)), ((11,3),(17,9))]
        self.area = self.get_area(self.points)
        self.grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 6, 6, 5, 5, 5, 5, 5, 5, 5, 3, 0, 0, 0],
                              [0, 0, 0, 5, 3, 5, 5, 5, 5, 5, 5, 6, 4, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 3, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 7, 5, 5, 5, 8, 6, 6, 6, 4, 5, 5, 5, 7, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 5, 7, 5, 8, 5, 4, 4, 4, 5, 4, 5, 7, 5, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0],
                              [2, 5, 5, 6, 5, 5, 5, 5, 5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 5, 5, 5, 5, 6, 6, 5, 5, 1],
                              [2, 5, 5, 6, 4, 5, 5, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 8, 5, 5, 5, 4, 5, 5, 5, 1],
                              [0, 0, 0, 5, 5, 0, 0, 0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 0, 0, 5, 5, 0, 0, 0],
                              [1, 5, 5, 5, 4, 5, 5, 5, 8, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 5, 5, 5, 4, 6, 5, 5, 2],
                              [1, 5, 5, 6, 6, 5, 5, 5, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 5, 5, 5, 5, 6, 5, 5, 2],
                              [0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 5, 7, 5, 4, 5, 4, 4, 4, 5, 8, 5, 7, 5, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 7, 5, 5, 5, 4, 6, 6, 6, 8, 5, 5, 5, 7, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, 5, 3, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 4, 6, 5, 5, 5, 5, 5, 5, 3, 5, 0, 0, 0],
                              [0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 6, 6, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 3, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


round = Turbo()
print(round.area)
