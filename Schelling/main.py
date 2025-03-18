import numpy as np
import matplotlib.pyplot as plt
import random

def create_grid(size, empty_ratio, group_ratio):
    #počty prvků v gridu
    num_empty = int(size * size * empty_ratio)
    num_group1 = int(size * size * group_ratio)
    num_group2 = int(size * size * group_ratio)
    num_group3 = size * size - num_empty - num_group1 - num_group2

    #vytvoření gridu
    grid = np.array([0] * num_empty + [1] * num_group1 + [2] * num_group2 + [3] * num_group3)
    #náhodné zamíchání gridu
    np.random.shuffle(grid)
    #převedení gridu na 2d pole
    return grid.reshape((size, size))

def get_neighbors_torus(grid, x, y):
    size = len(grid)
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % size, (y + dy) % size  # Wrap around for toroidal space
            neighbors.append(grid[nx, ny])
    return neighbors


def is_happy(grid, x, y, threshold):
    cell = grid[x, y]
    if cell == 0:
        return True
    neighbors = get_neighbors_torus(grid, x, y)
    same_type = sum(1 for n in neighbors if n == cell)
    return same_type / max(1, len(neighbors)) >= threshold


def move_unhappy(grid, threshold):
    size = len(grid)
    unhappy = [(x, y) for x in range(size) for y in range(size) if not is_happy(grid, x, y, threshold)]
    empty_cells = [(x, y) for x in range(size) for y in range(size) if grid[x, y] == 0]

    random.shuffle(unhappy)
    random.shuffle(empty_cells)

    for (x, y), (new_x, new_y) in zip(unhappy, empty_cells): #iterace přes pole tuplů
        grid[new_x, new_y] = grid[x, y]
        grid[x, y] = 0

def plot_grid(grid, iteration):
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    plt.title(f'Iteration {iteration}')
    plt.axis('off')
    plt.pause(0.1)


def simulate(size=50, empty_ratio=0.4, group_ratio=0.2, threshold=0.5, max_iters=10000):
    grid = create_grid(size, empty_ratio, group_ratio)
    plt.figure(figsize=(6, 6))

    happy_cells_iterations = []

    for i in range(max_iters):
        move_unhappy(grid, threshold)

        plot_grid(grid, i)
        happy_cells_iterations.append(sum(1 for x in range(size) for y in range(size) if is_happy(grid, x, y, threshold)))

        if all(is_happy(grid, x, y, threshold) for x in range(size) for y in range(size)):
            break

    plt.show()
    print(f"Covered in {len(happy_cells_iterations)} iterations")
    plt.plot(happy_cells_iterations)
    plt.show()


if __name__ == "__main__":
    simulate()

    #Vliv pammetru tol (treshhold) ?, Reprezentuje procento sousedů, kteří jsou stejného typu jako buňka, aby byla buňka šťastná.

    #Vývoj  # spokojenych jedinců v čase ? Viz plot

    #U jakého tol (treshhold) nastáva segregace? 0.3 / 30%

    #vliv velikosti okoli ? naiplmeentováno / předpoklad že segregace bude do větších celků bude více iterací

    #Možná rozšíření modeu ? další skupina