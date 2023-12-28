import math


def get_dist(pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
    '''Get the distance between 2 points'''
    return math.sqrt(abs(pos1[0] - pos2[0])**2 + abs(pos1[1] - pos2[1])**2)


def get_angle(frm: tuple[int, int], target: tuple[int, int]) -> float:
    '''Get the angle from point 1 to point 2, clockwise'''
    return math.atan2(target[1] - frm[1], target[0] - frm[0])


def get_mid_pt(pos1: tuple[int, int],
               pos2: tuple[int, int]) -> tuple[int, int]:
    '''Get the mid-point between 2 points'''
    return ((pos1[0] + pos2[0]) // 2, (pos1[1] + pos2[1]) // 2)
