import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
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
    """Ověří, zda je obarvení grafu G platné."""
    for u, v in G.edges():
        if col[u] == col[v]:
            return False
    return True

def cost(G: nx.Graph, col: List[int]) -> int:
    """Spočítá počet konfliktů v daném obarvení."""
    conflicts = 0
    for u, v in G.edges():
        if col[u] == col[v]:
            conflicts += 1
    return conflicts

def random_coloring(G: nx.Graph, k: int) -> List[int]:
    """Vytvoří náhodné obarvení."""
    return [random.randint(0, k - 1) for _ in range(G.number_of_nodes())]

def color(G: nx.Graph, k: int, steps: int) -> Tuple[List[int], bool]:
    """
    Pokusí se najít validní obarvení pomocí k barev
    pomocí lokálního prohledávání s kombinací náhodné procházky a hill climbing.
    """
    # Inicializace náhodného obarvení
    col = random_coloring(G, k)
    current_cost = cost(G, col)

    for step in range(steps):
        if current_cost == 0:
            print(f"Validní obarvení nalezeno ve {step}. kroku")
            return col, True

        # Vyber náhodný vrchol s konfliktem
        conflict_nodes = [u for u, v in G.edges() if col[u] == col[v]]
        if not conflict_nodes:
            break
        node = random.choice(conflict_nodes)

        # Zkus změnit barvu na jinou
        best_color = col[node]
        min_cost = current_cost
        for new_color in range(k):
            if new_color == col[node]:
                continue
            old_color = col[node]
            col[node] = new_color
            new_cost = cost(G, col)
            if new_cost < min_cost:
                min_cost = new_cost
                best_color = new_color
            col[node] = old_color  # revert

        # Hill climbing krok nebo náhodný krok
        if min_cost < current_cost or random.random() < 0.1:  # občasný random krok (simulované žíhání)
            col[node] = best_color
            current_cost = min_cost
        else:
            # náhodný krok - změň barvu libovolně
            col[node] = random.randint(0, k - 1)
            current_cost = cost(G, col)

    print(f"Počet konfliktů po {steps} krocích: {current_cost}")
    return col, current_cost == 0

if __name__ == "__main__":
    # Např.: G = load_dimacs_col("dsjc125.9.col")
    # Pro testování menšího grafu

    G = nx.Graph()
    G = readdimacs('dsjc125.9.col.txt')
    #G = readdimacs('test.txt')

    #G = nx.erdos_renyi_graph(15, 0.2)

    pos = nx.circular_layout(G)

    nx.draw(G, pos)
    plt.show()

    k = 5
    steps = 100000
    coloring, success = color(G, k, steps)

    print("Úspěšné obarvení:", success)
    print("Validita:", iscoloring(G, coloring))
    print("Barvy:", coloring)

