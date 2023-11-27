import random
from itertools import chain, combinations
from shapely.geometry import LineString, Point, Polygon


class MACHINE():
    """
        [ MACHINE ]
        MinMax Algorithm을 통해 수를 선택하는 객체.
        - 모든 Machine Turn마다 변수들이 업데이트 됨

        ** To Do **
        MinMax Algorithm을 이용하여 최적의 수를 찾는 알고리즘 생성
           - class 내에 함수를 추가할 수 있음
           - 최종 결과는 find_best_selection을 통해 Line 형태로 도출
               * Line: [(x1, y1), (x2, y2)] -> MACHINE class에서는 x값이 작은 점이 항상 왼쪽에 위치할 필요는 없음 (System이 organize 함)
    """
    def __init__(self, score=[0, 0], drawn_lines=[], whole_lines=[], whole_points=[], location=[]):
        self.id = "MACHINE"
        self.score = [0, 0] # USER, MACHINE
        self.drawn_lines = [] # Drawn Lines
        self.board_size = 7 # 7 x 7 Matrix
        self.num_dots = 0
        self.whole_points = []
        self.location = []
        self.triangles = [] # [(a, b), (c, d), (e, f)]

    def find_best_selection(self):
        print("selection begins")
        # count how many times each point has been used to draw lines so far
        points_to_drawn_times = { point: 0 for point in self.whole_points}

        # see the list of connected points to each point
        graph = { point: [] for point in self.whole_points }

        for (point1, point2) in self.drawn_lines:
            points_to_drawn_times[point1] += 1
            points_to_drawn_times[point2] += 1
            graph[point1].append((point1, point2))
            graph[point2].append((point1, point2))

        # reverse the key-value relation
        drawn_times_to_points = { points_to_drawn_times[point]: [] for point in points_to_drawn_times }
        for point in points_to_drawn_times:
            drawn_times_to_points[points_to_drawn_times[point]].append(point)
        
       
        # draw traingle if possible
        count_maximum_drawn__times = max(list(drawn_times_to_points.keys()))

        available = []
        
        available = self.find_lines_generating_two_triangles(graph)
        if len(available) > 0:
            return random.choice(available)        

        for drawn_times in range(count_maximum_drawn__times, 1, -1):
            if drawn_times in drawn_times_to_points:
                points = drawn_times_to_points[drawn_times]
                for point in points:
                    lines = graph[point]
                    available = self.find_best_triangle_lines(lines, graph)
                    if len(available) > 0:
                        return random.choice(available)

        if len(available) > 0:
            print("draw a traingle")
            return random.choice(available)

        # extract points that have not been used to draw any line yet
        points_not_drawn = drawn_times_to_points[0]

        # select 2 points that hasn't been used to draw a line
        if len(points_not_drawn) >= 2:
            print("draw using unused points")
            available = self.find_available(points_not_drawn)

        # pick among all the possible cases
        if len(available) == 0:
            available = self.find_available(self.whole_points)

        return random.choice(available)
    
    def find_available(self, points):
        return [[point1, point2] for (point1, point2) in list(combinations(points, 2)) if self.check_availability([point1, point2])]
    
    # todo: draw some line when user tries to fill the entire inner lines
    def find_best_triangle_lines(self, lines, graph):
        print("lines")
        print(lines)
        triangle_lines = []
        for [(point1, point2), (point3 ,point4)] in list(combinations(lines, 2)):
            print([(point1, point2), (point3 ,point4)])
            if self.are_points_same(point1, point3):
                if self.check_availability([point2, point4]):
                    if self.count_points_inside_triangle([(point1, point2), (point3, point4), (point2, point4)]) == 0 and len(self.find_lines_connecting_two_triangles([point1, point2, point4], graph)) == 0:
                        triangle_lines.append([point2, point4])
            elif self.are_points_same(point1, point4):
                if self.check_availability([point2, point3]):
                    if self.count_points_inside_triangle([(point1, point2), (point3, point4), (point2, point3)]) == 0 and len(self.find_lines_connecting_two_triangles([point1, point2, point3], graph)) == 0:
                        triangle_lines.append([point2, point3])
            elif self.are_points_same(point2, point3):
                if self.check_availability([point1, point4]):
                    if self.count_points_inside_triangle([(point1, point2), (point3, point4), (point1, point4)]) == 0 and len(self.find_lines_connecting_two_triangles([point1, point2, point4], graph)) == 0:
                        triangle_lines.append([point1, point4])
            else: # point 2 == point4
                if self.check_availability([point1, point3]):
                    if self.count_points_inside_triangle([(point1, point2), (point3, point4), (point1, point3)]) == 0 and len(self.find_lines_connecting_two_triangles([point1, point2, point3], graph)) == 0:
                        triangle_lines.append([point1, point3])
        print("triangle_lines")
        print(triangle_lines)
        return triangle_lines
        
    def count_points_inside_triangle(self, lines: list):
        triangle = self.organize_points(list(set(chain(*[lines[0], lines[1], lines[2]]))))
        count_points = 0
        for point in self.whole_points:
            if point in triangle:
                continue
            if self.is_point_inside_triangle(point, lines):
                count_points += 1
        print("number of points inside triangle")
        print(count_points)
        return count_points
    
    def is_point_inside_triangle(self, point: list, lines: list) -> bool:
        triangle = self.organize_points(list(set(chain(*[lines[0], lines[1], lines[2]]))))
        return bool(Polygon(triangle).intersection(Point(point)))
    
    def is_vertex_of_triangle(self, point: list, triangle: list) -> bool:
        return point in triangle
    
    def are_two_vertices_same(self, triangle1, triangle2):
        count_same_vertices = 0
        for point1 in triangle1:
            for point2 in triangle2:
                if point1[0] == point2[0] and point1[1] == point2[1]:
                    count_same_vertices += 1

        return count_same_vertices == 2
    
    def find_different_vertices(self, triangle1, triangle2):
        different_vertices = []
        points = triangle1 + triangle2
        for point in points:
            if point not in triangle1 or point not in triangle2:
                different_vertices.append(point)
        return different_vertices
        
    def find_lines_generating_two_triangles(self, graph):
        #find a line when the two triangles have the same two 
        triangle_lines = []
        for triangle in self.triangles:
            triangle_lines = triangle_lines + self.find_lines_connecting_two_triangles(triangle, graph)
        if len(triangle_lines) == 0:
            triangle_lines = self.find_lines_with_point_on_line()
        
        return triangle_lines
        
        
                        

        

    def find_lines_connecting_two_triangles(self, triangle, graph):
        triangle_lines = []
        
        print(triangle)
        for [vertex_in_triangle1, vertex_in_triangle2] in list(combinations(triangle, 2)):
            lines1 = graph[vertex_in_triangle1]
            lines2 = graph[vertex_in_triangle2]
            for [point1, point2] in lines1:
                for [point3, point4]  in lines2:
                    print("point1, point2 point3 point4")
                    print(point1, point2, point3, point4)
                    if self.are_points_same(point1, point3) and point1 not in triangle:
                        [vertex] = [vertex for vertex in triangle  if vertex not in [point1, point2, point3, point4]]
                        if self.check_availability([vertex, point1]):
                            triangle_lines.append([vertex, point1])
                    elif self.are_points_same(point1, point4) and point1 not in triangle:
                        [vertex] = [vertex for vertex in triangle  if vertex not in [point1, point2, point3, point4]]
                        if self.check_availability([vertex, point1]):
                            triangle_lines.append([vertex, point1])
                    elif self.are_points_same(point2, point3) and point2 not in triangle:
                        [vertex] = [vertex for vertex in triangle  if vertex not in [point1, point2, point3, point4]]
                        if self.check_availability([vertex, point2]):
                            triangle_lines.append([vertex, point2])
                    elif self.are_points_same(point2, point4) and point2 not in triangle:
                        [vertex] = [vertex for vertex in triangle  if vertex not in [point1, point2, point3, point4]]
                        if self.check_availability([vertex, point2]):
                            triangle_lines.append([vertex, point2])
        return triangle_lines
    
    def find_lines_with_point_on_line(self):
        triangle_lines = []
        # find a line when a point is in the middle of line
        for point in self.whole_points:
            for triangle in self.triangles:
                for line in list(combinations(triangle, 2)):
                    if self.is_point_on_line(point, line):
                        [left_vertex] = [vertex for vertex in triangle if vertex not in line]
                        if self.check_availability([point, left_vertex]):
                            triangle_lines.append([point, left_vertex])
        
        return triangle_lines

    def is_point_on_line(self, point, line):
        bool(LineString(line).intersects(Point(point)))

    def are_points_same(self, point1, point2):
        return point1[0] == point2[0] and point1[1] == point2[1]
    
    
    # Organization Functions
    def organize_points(self, point_list):
        point_list.sort(key=lambda x: (x[0], x[1]))
        return point_list
    
    def check_availability(self, line):
        line_string = LineString(line)

        # Must be one of the whole points
        condition1 = (line[0] in self.whole_points) and (line[1] in self.whole_points)
        
        # Must not skip a dot
        condition2 = True
        for point in self.whole_points:
            if point==line[0] or point==line[1]:
                continue
            else:
                if bool(line_string.intersection(Point(point))):
                    condition2 = False

        # Must not cross another line
        condition3 = True
        for l in self.drawn_lines:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in self.drawn_lines)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    

    
