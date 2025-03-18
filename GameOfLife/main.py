from numbers import Number
import random

class GameField:
    def __init__(self, field: Number) -> None:
        self.field = [random.choice([0,1]) for _ in range(field)]

    def __repr__(self):
        color_map = {0: '\033[91m█\033[0m', 1: '\033[92m█\033[0m'}  # Red for 0, Green for 1
        colored_string = ' '.join(color_map.get(char, str(char)) for char in self.field)
        return f"{colored_string}"
       # return ''.join(map(str, self.field))

    def step(self, surroundings_width) -> None:
        new_field = []
        for i in range(len(self.field)):
                match self.get_alive_neighbours(i):
                    case 0:
                        if(self.field[i] == 1):
                            new_field.append(0)
                        else:
                            new_field.append(0)
                    case 1:
                        if (self.field[i] == 1):
                            new_field.append(1)
                        else:
                            new_field.append(0)
                    case 2:
                        if (self.field[i] == 1):
                            new_field.append(1)
                        else:
                            new_field.append(1)
                    case 3:
                        if (self.field[i] == 1):
                            new_field.append(0)
                        else:
                            new_field.append(0)
                    case 4:
                        if (self.field[i] == 1):
                            new_field.append(0)
                        else:
                            new_field.append(0)
                    case _:
                        break
        self.field = new_field

    def get_alive_neighbours(self, i) -> Number:
        if i+2 >= len(self.field) or i-2 < 0:
            return 0
        return self.field[i-1] + self.field[i-2] + self.field[i+1] + self.field[i+2]


class Game:
    def __init__(self, field_len: Number, surroundings_width: Number, generations: Number) -> None:
        self.field = GameField(field_len)
        self.surroundings_width = surroundings_width,
        self.generations = generations

    def run(self):
        for _ in range(self.generations):
            self.field.step(self.surroundings_width)
            print(self.field)


if __name__ == '__main__':
    game = Game(50, 1, 10)
    game.run()