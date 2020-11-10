import random
from typing import List


class MiniMap:

    def __init__(self, name: str, level: int):
        self.name = name
        #  count of Fire and  Med = level
        #  count of Mill. Bases,city = level*2
        self.level = level
        #  square 12 by 12 chunks
        self.MAP_SIZE = 20
        # empty map
        self.map: List[List[str]] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], ]
        # chose boat
        self.boat = level
        print('was created minimap: ', self.name)

    @staticmethod
    def near_chunks_values(x, y, list_of_chunk):
        values = [
            list_of_chunk[y + 1][x - 1], list_of_chunk[y + 1][x],
            list_of_chunk[y + 1][x + 1],  # up side
            list_of_chunk[y][x - 1],  # right
            list_of_chunk[y][x + 1],  # left
            list_of_chunk[y - 1][x - 1], list_of_chunk[y - 1][x],
            list_of_chunk[y - 1][x + 1]  # down side
        ]
        return values

    # fill map by forest
    def __generate_default_map__(self):
        for y in range(self.MAP_SIZE):
            for x in range(self.MAP_SIZE):
                self.map[y].append(' #')

    # add locations to map
    def __set_locations__(self, name: str, count: int):
        i = 0
        while i < count:
            x = random.randrange(self.MAP_SIZE - 1)
            y = random.randrange(self.MAP_SIZE - 1)
            # get chunk with random cords

            if self.map[y][x] in {' F', ' M', ' C', ' B', ' T', ' N'}:
                continue
            else:
                # locations cant be nearer then 1 chunk
                all_not_loc = True
                for val in self.near_chunks_values(x,y,self.map):
                    if val in {' F', ' M', ' C', ' B', ' T', ' N'}:
                        all_not_loc = False
                        break
                if all_not_loc:
                    self.map[y][x] = name
                    i += 1

    # get all locations on vertical Axe
    def __get_locations_on_x__(self, x: int):
        loc: List[int] = []
        for y in range(self.MAP_SIZE):
            if self.map[y][x] not in {' #', ' H', ' s', }:
                loc.append(y)
        return loc

    #  get all locations on Horizontal Axe
    def __get_locations_on_y__(self, y: int):
        loc: List[int] = []
        for x in range(self.MAP_SIZE):
            if self.map[y][x] not in {' #', ' H', ' s', ' |'}:
                loc.append(x)
        return loc

    def __build_road_on_x__(self, x: int, start_y: int, end_y: int):
        for y in range(start_y + 1, end_y):
            if self.map[y][x] == '--':
                continue
            else:
                self.map[y][x] = ' |'

    def __build_road_on_y__(self, y: int, start_x: int, end_x: int):
        for x in range(start_x + 1, end_x):
            self.map[y][x] = '--'

        if self.map[y][end_x] == ' |':
            self.map[y][end_x] = ' +'

    # build roads, connect cites
    def __create_roads__(self):
        # create verticals roads ( ' |' ) X
        for x in range(self.MAP_SIZE):
            loc = self.__get_locations_on_x__(x)
            length = len(loc)
            if length > 1:
                # connect location
                self.__build_road_on_x__(x, loc[0], loc[1])
                for i in range(2, length):
                    # check distance length of two roads
                    if loc[i] - loc[i - 1] < (loc[i - 1] - loc[i - 2]) + 2:
                        self.__build_road_on_x__(x, loc[i - 1], loc[i])
        # create horizontal roads ( '--' ) Y
        for y in range(self.MAP_SIZE):
            loc = self.__get_locations_on_y__(y)
            length = len(loc)
            if length > 1:
                # connect only  two location
                self.__build_road_on_y__(y, loc[0], loc[1])
                for i in range(2, length):
                    if loc[i] - loc[i - 1] < (loc[i - 1] - loc[i - 2]) + 2:
                        self.__build_road_on_y__(y, loc[i - 1], loc[i])

    # generate city fire med mil town
    def __procedure_generate__(self):
        towns_number = 6 // self.level + 2
        # add town
        self.__set_locations__(' T', towns_number)
        # add City
        self.__set_locations__(' C', self.level + 3)

        # add Fire Station
        self.__set_locations__(' F', self.level)

        # add Hospitals
        self.__set_locations__(' M', self.level)
        # connect locations and s.
        self.__create_roads__()
        # MILITARY BASES USUALLY DON'T CONNECTED BY ROAD so they generated after

        # add Nato Bases
        self.__set_locations__(' N', self.level - 1)

        # add Soviet Bases
        self.__set_locations__(' B', self.level - 1)

    # add secret location
    def __add_secret__(self):
        while True:
            # select random chunk except border
            x = random.randrange(1, self.MAP_SIZE - 1)
            y = random.randrange(1, self.MAP_SIZE - 1)

            if self.map[y][x] == ' #':
                all_forest = True
                # all near chunk must be forest
                # secret cant be generated
                for val in self.near_chunks_values(x,y,self.map):
                    if val != ' #':
                        all_forest = False
                        break
                if all_forest:
                    self.map[y][x] = ' s'
                    break

    # add one or more copter
    def __add_helicopter__(self):
        # number of copter == level
        i = 0
        while i < self.level - 1:
            x = random.randrange(self.MAP_SIZE)
            y = random.randrange(self.MAP_SIZE)
            # get chunk with random cords
            chunk: str = self.map[y][x]
            # H. can spawn only in forest
            if chunk == ' #':
                self.map[y][x] = ' H'
                # add H. and move to another
                i += 1

    # add boat in opposite side
    def __add_boat__(self):
        y = random.randrange(self.MAP_SIZE)
        print(' boat has been added in ', y)

    # Do all Gen. stage
    def gen_map(self):
        print('generate default map')
        self.__generate_default_map__()
        print('generate Locations and road')
        self.__procedure_generate__()
        print('add Helicopter')
        self.__add_helicopter__()
        print('add Secret')
        self.__add_secret__()
        print('add Boat')
        self.__add_boat__()

    # display map
    def print_map(self):
        for row in self.map:
            print(' '.join(map(str, row)))
        print('\n')


if __name__ == '__main__':
    minimap = MiniMap('new map', 1)
    minimap.gen_map()
    minimap.print_map()
    # show info about map
    print(f'''
count of Cites C {minimap.level + 3}

count of Towns T {12 // minimap.level + 2}

count of Fire Stations F {minimap.level}

count of Hospitals M {minimap.level}

count of Nato military bases  N {minimap.level - 1}

count of Soviet  military bases  B {minimap.level - 1}

count of Helicopters H {minimap.level - 1}
''')
