import networkx as nx
import time
import random
from typing import List, Tuple

def readdimacs(filename):
    file = open(filename, 'r')
    lines = file.readlines()

    Gd = nx.Graph()

    for line in lines:
        if line[0] == "e":
            vs = [int(s) for s in line.split() if s.isdigit()]
            Gd.add_edge(vs[0] - 1, vs[1] - 1)
    return Gd


def iscoloring(G: nx.Graph, col: List[int]) -> bool:
    #je obarvení validní
    for u, v in G.edges():
        if col[u] == col[v]:
            return False
    return True

def cost(G: nx.Graph, col: List[int]) -> int:
    #počet konfliktů
    conflicts = 0
    for u, v in G.edges():
        if col[u] == col[v]:
            conflicts += 1
    return conflicts

def random_coloring(G: nx.Graph, k: int) -> List[int]:
    #random obarvení
    return [random.randint(0, k - 1) for _ in range(G.number_of_nodes())]

def color(G: nx.Graph, k: int, steps: int) -> Tuple[List[int], bool, float]:
    start_time = time.time()
    #lokální prohledávání s ochlazováním
    col = random_coloring(G, k)
    current_cost = cost(G, col)

    initial_temp = 0.3  # počáteční pravděpodobnost náhodného kroku
    final_temp = 0.01   # konečná minimální pravděpodobnost

    for step in range(steps):
        if current_cost == 0:
            print(f"Validní obarvení nalezeno ve {step}. kroku")
            return col, True, time.time() - start_time

        # Lineární ochlazování
        temperature = initial_temp - ((initial_temp - final_temp) * (step / steps))
        temperature = max(temperature, final_temp)

        # Vyber náhodný konflikt
        conflict_edges = [(u, v) for u, v in G.edges() if col[u] == col[v]]
        if not conflict_edges:
            break
        u, v = random.choice(conflict_edges)
        node = random.choice([u, v])

        # Hledání nejlepší barvy pro snížení konfliktů
        best_color = col[node]
        min_cost = current_cost
        for new_color in range(k): #projít všechny barvy
            if new_color == col[node]:
                continue
            old_color = col[node]
            col[node] = new_color
            new_cost = cost(G, col)
            if new_cost < min_cost:
                min_cost = new_cost
                best_color = new_color
            col[node] = old_color  # revert

        # Rozhodnutí: přijmout lepší nebo náhodně zhoršit
        if min_cost < current_cost or random.random() < temperature:
            col[node] = best_color if min_cost < current_cost else random.randint(0, k - 1)
            current_cost = cost(G, col)

        if step % (steps // 10) == 0:
            print(f"Krok {step}/{steps}, konflikty: {current_cost}, temp: {temperature:.4f}, čas: {time.time() - start_time:.2f}s")

    print(f"Počet konfliktů po {steps} krocích: {current_cost}")
    return col, current_cost == 0, time.time() - start_time

def findLowestColour(noColor: int, maxRunsPerColor: int, Gx: nx.Graph ):
    run = True
    while run:
        for i in range(maxRunsPerColor):

            steps = 100000

            coloring, success, time = color(Gx, noColor, steps)

            print("Úspěšné obarvení:", success)
            print("Validita:", iscoloring(Gx, coloring))
            print("Barvy:", coloring)
            print("Počet barev:", len(set(coloring)))
            print("Čas:", time)

            if(success):
                noColor = noColor - 1
                break
        if(success == False):
            run = False


if __name__ == "__main__":
    #Gx = readdimacs('dsjc125.9.col.txt')

    Gx = readdimacs('test.txt')


    findLowestColour(5, 10, Gx)





