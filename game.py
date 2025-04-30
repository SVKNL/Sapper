from random import sample


class Cell:
    def __init__(self):
        self.is_opened = False
        self.is_bomb = False
        self.nearby_bombs = 0

    def draw(self):
        if self.is_opened:
            return ' ' if self.nearby_bombs == 0 else str(self.nearby_bombs)
        else:
            return '*'


class GameField:
    def __init__(self, rows, columns, bombs_number):
        self.rows = rows
        self.columns = columns
        self.bombs_number = bombs_number
        self.field = [[Cell() for _ in range(self.columns)]
                      for _ in range(self.rows)]
        self.is_bombed = False

    def is_cell_in_field(self, x, y):
        return 0 <= y < self.columns and 0 <= x < self.rows

    def find_neighbors(self, x, y):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                n_x, n_y = x + i, y + j
                if (i != 0 or j != 0) and self.is_cell_in_field(n_x, n_y):
                    neighbors.append((n_x, n_y))
        return neighbors

    def plant_bombs(self, initial_x, initial_y):
        initial_coordinates = (initial_x, initial_y)
        available_coordinates = ([(row, column)
                                  for row in range(self.rows)
                                  for column in range(self.columns)])
        available_coordinates.remove(initial_coordinates)
        bombs = sample(available_coordinates, self.bombs_number)
        for row, column in bombs:
            self.field[row][column].is_bomb = True

        self.is_bombed = True

    def count_nearby_mines(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if not self.field[row][column].is_bomb:
                    counter = 0
                    for x, y in self.find_neighbors(row, column):
                        if self.field[x][y].is_bomb:
                            counter += 1
                    self.field[row][column].nearby_bombs = counter

    def handle_step(self, x, y):
        if not self.is_cell_in_field(x, y):
            print('Wrong coordinates')
            return True
        if not self.is_bombed:
            self.plant_bombs(x, y)
            self.count_nearby_mines()
        cell = self.field[x][y]
        if cell.is_opened:
            print('Cell is already opened')
            return True
        cell.is_opened = True
        if cell.is_bomb == True:
            print('Lose')
            return False
        if cell.nearby_bombs == 0:
            for n_x, n_y in self.find_neighbors(x, y):
                neighbor = self.field[n_x][n_y]
                if not neighbor.is_opened:
                    self.handle_step(n_x, n_y)
        return True

    def draw_field(self):
        print("  " + " ".join(f"{i}" for i in range(self.rows)))
        for row in range(self.columns):
            row_to_display =[]
            for col in range(self.rows):
                row_to_display.append(self.field[col][row].draw())
            print(f"{row} " + " ".join(row_to_display))

    def is_win(self):
        opened_cells = sum(
            1
            for row in range(self.rows)
            for column in range(self.columns)
            if self.field[row][column].is_opened
        )
        return opened_cells == self.rows * self.columns - self.bombs_number


class ConsoleInterface:
    def __init__(self):
        print("Game started")

    def start_game(self):
        try:
            rows = int(input("Enter number of rows: \n "))
            cols = int(input("Enter number of columns: \n "))
            mines = int(input("Enter number of mines: \n "))
            if mines >= rows * cols:
                print("Too much mines")
                return
            game_field = GameField(cols, rows, mines)
            while True:
                command = (input("Enter command: open X Y or show or exit: \n")
                           .strip().lower())
                if command == 'exit':
                    break
                elif command == 'show':
                    game_field.draw_field()
                elif command.startswith('open'):
                    command_words = command.split()
                    if len(command_words) != 3:
                        print("Wrong command")
                        continue
                    try:
                        x = int(command_words[1])
                        y = int(command_words[2])
                    except ValueError:
                        print("Wrong coordinates")
                        continue
                    step_status = game_field.handle_step(x, y)
                    game_field.draw_field()
                    if not step_status:
                        break
                    elif game_field.is_win():
                        print("Win")
                        break
                else:
                    print("Wrong command")
        except ValueError:
            print("Wrong command")


if __name__ == "__main__":
    interface = ConsoleInterface()
    interface.start_game()










