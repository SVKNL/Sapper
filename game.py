from random import sample



class SapperGame:
    def __init__(self, field_size=(3, 3), bombs_number=4, initial_coordinates=None):
        self.initial_coordinates = initial_coordinates
        self.field_size = field_size
        self.bombs_number = bombs_number
        if self.field_size[0] * self.field_size[1] <= self.bombs_number:
            raise  ValueError('Мин больше, чем слотов')
        self.opened_sections = {}
        self.field_coordinates = self.generate_field_coordinates()
        self.steps_counter = 0
        self.unopened_sections = self.generate_unopened_sections()


    def generate_field_coordinates(self):
        field_coordinates = []
        for i in range(self.field_size[0]):
            for j in range(self.field_size[1]):
                field_coordinates.append((i, j))
        if self.initial_coordinates:
            field_coordinates.remove(self.initial_coordinates)
            return field_coordinates
        return field_coordinates


    def generate_unopened_sections(self):
        unopened_sections = {}
        bombs = sample(self.field_coordinates, self.bombs_number)
        for coordinate in self.field_coordinates:
            if coordinate in bombs:
                unopened_sections[coordinate] = True
            else:
                unopened_sections[coordinate] = False
        return unopened_sections


    def handle_right_step(self, coordinates, exclusion=None):
        if not exclusion:
            exclusion = (coordinates,)
        neighbours = []
        is_recursion = True
        for x in range(-1, 2):
            for y in range(-1, 2):
               n_x = coordinates[0] + x
               n_y = coordinates[1] + y
               if ((n_x, n_y) not in self.opened_sections
                       and 0 <= n_x < self.field_size[0]
                       and 0 <= n_y < self.field_size[1]
                       and (n_x, n_y) not in exclusion):
                    neighbour = (n_x, n_y)
                    neighbours.append(neighbour)
                    if self.unopened_sections.get(neighbour):
                        is_recursion = False
        if is_recursion and neighbours:
            self.opened_sections[coordinates] = ' '
            for neighbour in neighbours:
                if neighbour not in self.opened_sections:
                    self.handle_right_step(neighbour, (coordinates, neighbour))
        else:
            bomb_counter  = 0
            for neighbour in neighbours:
                if self.unopened_sections[neighbour]:
                    bomb_counter += 1
            self.opened_sections[coordinates] = bomb_counter
            if self.initial_coordinates and self.initial_coordinates != coordinates:
                self.unopened_sections.pop(coordinates)


    def is_good_step(self, coordinates):
        if self.unopened_sections[coordinates]:
            return False
        return True


    def is_over(self):
        if (len(self.opened_sections) ==
                self.field_size[0] * self.field_size[1] - self.bombs_number):
            return True
        return False


    def draw_field(self):
        first_row = ''.join(str(i) for i in range(0, self.field_size[0]))
        print('  ' + first_row)
        print("".join("_" for i in range(self.field_size[0] + 2)))
        for y in range(self.field_size[1]):
            row = ''
            for x in range(self.field_size[0]):
                if (x, y) in self.opened_sections:
                    row += str(self.opened_sections[(x, y)])
                else:
                    row += '*'
            print(str(y) + '|' + row)


while True:
    x_size, y_size = input('Введите размеры поля в формате X Y')
    field_size = (int(x_size), int(y_size))
    bombs_number = int(input('Enter bombs number'))
    start = SapperGame(field_size, bombs_number)
    start.draw_field()
    x, y = input('Enter coordinates: \n')
    initial_coordinates = (int(x), int(y))
    main_game = SapperGame(field_size, bombs_number, initial_coordinates)
    main_game.handle_right_step(initial_coordinates)
    main_game.draw_field()
    while True:
        try:
            x, y = input('Enter coordinates: \n')
            coordinates = (int(x), int(y))
            if main_game.is_good_step(coordinates):
                main_game.handle_right_step(coordinates)
                if main_game.is_over():
                    print('Win')
                    break
                main_game.draw_field()
            else:
                print('Lose')
                break
        except:
            x, y = input('Enter correct coordinates: \n')
            coordinates = (int(x), int(y))
            if main_game.is_good_step(coordinates):
                main_game.handle_right_step(coordinates)
                if main_game.is_over():
                    print('Win')
                main_game.draw_field()
            else:
                print('Lose')
                break









