from typing import Optional
import math


class Mask:
    '''
        Represents a mask of any game objects, mainly used for colliders

        Parameters
        ----------
        width `int`:
            width of the object
        height `int`:
            height of the object
        radius `int`:
            radius of the circle, if provided, the object is classified as a circle
        corners `list`[`tuple`(`int`, `int`)]:
            The corners of the polygon provided as a list of relative coordinates, None if the object is a circle
        
        Attributes
        ----------
        size: (width, height)
            The size of the mask
        center: (center_x, center_y)
            The coordinates of the center of the mask
    '''

    def __init__(self,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 radius: Optional[int] = None,
                 corners: Optional[list[tuple[int, int]]] = None
                 ) -> None:
        if corners and radius:
            raise ValueError("Only radius or corners should be provided")
        elif (not width or not height) and not radius and not corners:
            raise ValueError(
                "width and height must be provided if neither radius nor corners are provided")
        self.radius = radius
        self.corners = corners
        if corners:
            x_coordinates = list(map(lambda x: x[0], corners))
            y_coordinates = list(map(lambda x: x[1], corners))
            self.size = self.width, self.height = max(
                x_coordinates), max(y_coordinates)
            self.center = self.center_x, self.center_y = sum(
                x_coordinates) / len(x_coordinates), sum(y_coordinates) / len(y_coordinates)
        elif radius:
            self.center = self.center_x, self.center_y = radius, radius
            self.size = self.width, self.height = radius * 2, radius * 2
        else:
            self.size = self.width, self.height = width, height
            self.center = self.center_x, self.center_y = self.width/2 if self.width else 0, self.height/2 if self.height else 0
            self.corners = [(0, 0), (0, height), (width, height), (width, 0)]

    def rotate(self, degrees, pivot: Optional[tuple[int, int]]):
        if not self.corners:
            return
        theta = math.radians(degrees)
        cosang, sinang = math.cos(theta), math.sin(theta)

        # find center point of Polygon to use as pivot or use provided pivot
        if not pivot:
            number_of_corners = len(self.corners)
            pivot_x = sum(point[0]
                          for point in self.corners) / number_of_corners
            pivot_y = sum(point[1]
                          for point in self.corners) / number_of_corners
        else:
            pivot_x, pivot_y = pivot

        # Calculate new corners
        new_corners = []
        for p in self.corners:
            x, y = p[0], p[1]
            tx, ty = x - pivot_x, y - pivot_y
            new_x = (tx * cosang + ty * sinang) + pivot_x
            new_y = (-tx * sinang + ty * cosang) + pivot_y
            new_corners.append((new_x, new_y))

        # Update attributes
        self.corners = new_corners
        x_coordinates = map(lambda x: x[0], new_corners)
        y_coordinates = map(lambda x: x[1], new_corners)
        self.size = self.width, self.height = max(
            x_coordinates), max(y_coordinates)
        self.center = self.center_x, self.center_y = sum(
            x_coordinates) / len(list(x_coordinates)), sum(y_coordinates) / len(list(y_coordinates))

    def get_centerx(self, obj_x:int) -> int:
        return round(obj_x + self.center_x)

    def get_centery(self, obj_y:int) -> int:
        return round(obj_y + self.center_y)