import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

rng = np.random.default_rng(12345)  # seed

def readdimacs(filename):
    file = open(filename, 'r')
    lines = file.readlines()

    Gd = nx.Graph()

    for line in lines:
        if line[0] == "e":
            vs = [int(s) for s in line.split() if s.isdigit()]
            Gd.add_edge(vs[0] - 1, vs[1] - 1)
    return Gd

# bere na vstupu pole barev vrcholu poporade, cislum priradi nahodne barvy a vykresli graf
def plot(G, cols):
    k = np.max(cols)
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    colmap = ["#" + ''.join(rng.choice(symbols, 6)) for i in range(k + 1)]

    colors = [colmap[c] for c in cols]

    nx.draw(G, node_color=colors, with_labels=True)

    plt.show()

if __name__ == '__main__':
    Gx = readdimacs('dsjc125.1.col.txt')
    colours = [4, 1, 3, 4, 2, 2, 3, 3, 3, 1, 2, 3, 3, 4, 0, 2, 3, 0, 1, 0, 0, 2, 4, 2, 4, 1, 4, 4, 0, 1, 3, 4, 0, 1, 1, 2, 1, 1, 2, 4, 0, 0, 2, 0, 1, 0, 4, 3, 4, 3, 2, 0, 3, 4, 1, 4, 0, 2, 3, 1, 1, 0, 4, 3, 4, 2, 0, 4, 1, 2, 1, 0, 1, 1, 3, 0, 4, 3, 0, 2, 2, 0, 2, 1, 1, 1, 3, 4, 3, 1, 1, 3, 4, 4, 0, 0, 3, 0, 2, 0, 0, 4, 0, 3, 0, 1, 3, 1, 0, 2, 2, 0, 2, 3, 1, 2, 4, 3, 0, 3, 1, 4, 1, 3, 3]

    #Gx = readdimacs('test.txt')
    #colours =[0, 1, 1, 2, 0]

    plot(Gx, colours)
