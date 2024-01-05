import math
from typing import overload
def vec_addition(vec1:tuple[int|float, int|float], vec2:tuple[int|float, int|float]):
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])

def vec_subtraction(vec1:tuple[int|float, int|float], vec2:tuple[int|float, int|float]):
    return (vec1[0] - vec2[0], vec1[1] - vec2[1])

def vec_orthogonal(vec:tuple[int|float, int|float]):
    return (vec[1], -vec[0])

def vec_opposite(vec:tuple[int|float, int|float]):
    return (-vec[0], -vec[1])

def vec_normalize(vec:tuple[int|float, int|float]):
    """
    :return: The vector scaled to a length of 1
    """
    norm = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
    return vec[0] / norm, vec[1] / norm

def get_dist(pos1: tuple[int|float, int|float], pos2: tuple[int|float, int|float]) -> float:
    '''Get the distance between 2 points'''
    return math.sqrt(abs(pos1[0] - pos2[0])**2 + abs(pos1[1] - pos2[1])**2)


def get_angle(frm: tuple[int|float, int|float], target: tuple[int|float, int|float]) -> float:
    '''Get the angle from point 1 to point 2, clockwise'''
    return math.atan2(target[1] - frm[1], target[0] - frm[0])


def get_mid_pt(pos1: tuple[int|float, int|float],
               pos2: tuple[int|float, int|float]) -> tuple[int, int]:
    '''Get the mid-point between 2 points'''
    return (round(pos1[0] + pos2[0]) // 2, round(pos1[1] + pos2[1]) // 2)


def resolve(magnitude: int | float, angle: float):
    '''Return the resolved components of the vector as a tuple of (x, y)'''
    return (magnitude * math.cos(angle), magnitude * math.sin(angle))


def point_to_line_distance(
        point: tuple[int|float, int|float], line: tuple[tuple[int|float, int|float], tuple[int|float, int|float] | float]):
    '''Return the distance from a point to a line

    Parameters
    ----------
    point:
        The point to calculate distance to
    line: `tuple`[`tuple`[`int`, `int`] | `float`]:
        A line defined by 2 points or a point that the line passes through with an angle

    Returns
    -------
    distance `float`:
        If the distance is +ve, the distance is 90deg anti-clockwise to the line\n
        If the distance is -ve, the distance is 90deg clockwise to the line'''
    if isinstance(line[1], float | int):
        line_point, angle = line[0], line[1]
        return math.cos(
            angle) * (line_point[1] - point[1]) - math.sin(angle) * (line_point[0] - point[0])

    elif isinstance(line[1], tuple):
        line_pt_1, line_pt_2 = line
        if not isinstance(
                line_pt_1,
                tuple) or not isinstance(
                line_pt_2,
                tuple):
            raise TypeError("Line points must be a tuple")
        return ((line_pt_2[0] - line_pt_1[0]) * (line_pt_1[1] - point[1]) - (line_pt_1[0] - point[0]) * (
            line_pt_2[1] - line_pt_1[1])) / math.sqrt((line_pt_2[0] - line_pt_1[0]) ** 2 + (line_pt_2[1] - line_pt_1[1]) ** 2)

    else:
        raise TypeError(
            "line type must be either 'float' or 'tuple[int, int]'")
