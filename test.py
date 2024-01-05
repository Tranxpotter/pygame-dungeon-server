# def edge_direction(point0, point1):
#     """
#     :return: A vector going from point0 to point1
#     """
#     return point1[0] - point0[0], point1[1] - point0[1]

# def vertices_to_edges(vertices):
#     """
#     :return: A list of the edges of the vertices as vectors
#     """
#     return [edge_direction(vertices[i], vertices[(i + 1) % len(vertices)])
#             for i in range(len(vertices))]

# vertices = [(0, 0), (1, 2), (3, 5), (2, 1)]

# print(vertices_to_edges(vertices))
# import math
# def point_to_line_distance(point:tuple[int, int], line_point:tuple[int, int], angle:float):
#     return math.cos(angle)*(line_point[1] - point[1]) - math.sin(angle)*(line_point[0] - point[0])

# print(point_to_line_distance((3, 1), (1, 1), math.radians(30 - 90)))
# import math
# from engine.utils import point_to_line_distance
# from engine.mask import Mask
# def move(dt: float, speed, angle, mask:Mask):
#     while angle >= 2 * math.pi:
#         angle -= 2 * math.pi
#     move_distance = speed * dt
#     move_x = round(move_distance * math.cos(angle), 1)
#     move_y = round(move_distance * math.sin(angle), 1)

#     print(f"{move_x=}, {move_y=}")

#     if mask.radius:
#         '''Circle stuff'''

#     elif mask.corners:
#         center = mask.center
#         corners = mask.corners

#         points_distance = [(corner, round(point_to_line_distance(corner, (center, angle)), 1)) for corner in corners]
#         distances = list(map(lambda x:x[1], points_distance))

#         furthest_points = [
#             [corner for corner, _ in filter(lambda x: x[1] == max(distances), points_distance)], 
#             [corner for corner, _ in filter(lambda x: x[1] == min(distances), points_distance)]
#         ] #[0] are +ve, [1] and -ve
#         print(f"{furthest_points=}")
#         new_line = (furthest_points[1][0], furthest_points[0][0])
        
#         #Line adjustment due to other points having the same distance from center line
#         no_projection_corners = []
#         if len(furthest_points[0]) > 1:
#             keep_corner = furthest_points[0][0]
#             no_projection_corners.append(keep_corner)
#             longest_distance = 0
#             for corner in furthest_points[0][1::]:
#                 distance = point_to_line_distance(corner, new_line)
#                 if distance > longest_distance:
#                     no_projection_corners.append(corner)
#                     try:
#                         no_projection_corners.remove(keep_corner)
#                     except ValueError:
#                         pass
#                     keep_corner = corner
#                     longest_distance = distance
            
#             new_line = (new_line[0], keep_corner)
        
#         if len(furthest_points[1]) > 1:
#             keep_corner = furthest_points[1][0]
#             no_projection_corners.append(keep_corner)
#             longest_distance = 0
#             for corner in furthest_points[1][1::]:
#                 distance = point_to_line_distance(corner, new_line)
#                 if distance > longest_distance:
#                     no_projection_corners.append(corner)
#                     try:
#                         no_projection_corners.remove(keep_corner)
#                     except ValueError:
#                         pass
#                     keep_corner = corner
#                     longest_distance = distance

#             new_line = (keep_corner, new_line[1])
#         print(f"{new_line=}")
#         print(f"{no_projection_corners=}")

#         new_polygon_corners = []
#         for corner in corners:
#             distance = point_to_line_distance(corner, new_line)
#             if distance > 0 or corner in no_projection_corners:
#                 new_polygon_corners.append(corner)
#             elif distance < 0 and corner:
#                 new_polygon_corners.append((corner[0] + move_x, corner[1] + move_y))
#             else:
#                 if angle >= 1:
#                     new_polygon_corners.append((corner[0] + move_x, corner[1] + move_y))
#                     new_polygon_corners.append(corner)
#                 else:
#                     new_polygon_corners.append(corner)
#                     new_polygon_corners.append((corner[0] + move_x, corner[1] + move_y))
        
#         print(new_polygon_corners)


# # mask = Mask(corners=[(1, 0), (2, 1), (0, 1)])
# mask = Mask(2, 2)
# move(1, 10, math.radians(0), mask)



from engine.collider import FastCollider
from engine.mask import Mask
mask = Mask(corners=[(1, 0), (2, 1), (0, 1)])
collider = FastCollider([0], mask)
collider.on_move((1, 1))
print(collider.mask.corners)