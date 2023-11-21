import random
from itertools import combinations
from shapely.geometry import LineString, Point

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

        # count how many times each point has been used to draw lines so far
        points_to_drawn_times = { point: 0 for point in self.whole_points}
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
        
        # extract points that have not been used to draw any line yet
        points_not_drawn = drawn_times_to_points[0]

        print(graph)

        print(drawn_times_to_points)

        # draw traingle if possible
        count_maximum_drawn__times = max(list(drawn_times_to_points.keys()))

        print(count_maximum_drawn__times)

        available = []

        
        
                

        for drawn_times in range(count_maximum_drawn__times, 1, -1):
            points = drawn_times_to_points[drawn_times]
            print(points)
            for point in points:
                lines = graph[point]
                print(lines)
                for [(point1, point2), (point3 ,point4)] in list(combinations(lines, 2)):
                    print([(point1, point2), (point3 ,point4)])
                    if point1[0] == point3[0] and point1[1] == point3[1]:
                        if self.check_availability([point2, point4]):
                            available.append([point2, point4])
                    elif point1[0] == point4[0] and point1[1] == point4[1]:
                        if self.check_availability([point2, point3]):
                            available.append([point2, point3])
                    elif point2[0] == point3[0] and point2[1] == point3[1]:
                        if self.check_availability([point1, point4]):
                            available.append([point1, point4])
                    else: # point 2 == point4
                        if self.check_availability([point1, point3]):
                            available.append([point1, point3])
                    print(available)
        
        if len(available) != 0:
            return random.choice(available)

        # select 2 points that hasn't been used to draw a line
        if len(points_not_drawn) >= 2:
            available = self.find_available(points_not_drawn)
            return random.choice(available)

        # pick among all the possible cases
        if len(available) == 0:
            available = self.find_available(self.whole_points)


    
        return random.choice(available)
    
    def find_available(self, points):
        return [[point1, point2] for (point1, point2) in list(combinations(points, 2)) if self.check_availability([point1, point2])]
    
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

    
