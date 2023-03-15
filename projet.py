from collections import deque
import time

# la classe Node represente un etat du problème


class Node:
    toLeft = ''
    toRight = ''

    # constructeur
    def __init__(self, C_g, M_g, C_d, M_d):
        # C_g -> cannibales sur la rive gauche
        # M_g -> missionnaires sur la rive gauche
        # C_d -> cannibales sur la rive droite
        # M_d -> missionnaires sur la rive droite
        self.C_g = C_g
        self.M_g = M_g
        self.C_d = C_d
        self.M_d = M_d

    # methodes permettant d'utiliser Node dans des structures de donnees (ici: dictionnaire et ensemble)

    def __eq__(self, other):
        return self.C_g == other.C_g and self.M_g == other.M_g and self.C_d == other.C_d and self.M_d == other.M_d

    # permet de determiner si 2 noeuds sont equivalents avec leur table de hachage
    def __hash__(self):
        return hash((self.C_g, self.M_g, self.C_d, self.M_d))

    def __str__(self):
        return f'M_g={self.M_g}, C_g={self.C_g}|M_d={self.M_d}, C_d={self.C_d}'

    # methode permettant de definir si un etat est valide
    # contrainte principale : le nombre de Missionnaires ne doit jamais être strictement inferieure au nombre de Cannibales
    def is_valid(self):
        return (self.M_g == 0 or self.M_g >= self.C_g) and (self.M_d == 0 or self.M_d >= self.C_d)


# la classe Graph represente le graphe de recherche
class Graph:
    visited = {}  # noeuds dejà traites
    queued = {}  # noeuds à traiter
    states = []  # sous-noeuds à traiter avant d'être empiles dans queued
    parent = {}  # dictionnaire qui indexe les parents de chaque noeud

    def __init__(self, start, end, maxp_boats):
        self.start = start
        self.end = end
        self.maxp_boats = maxp_boats

    # la methode get_next_states retourne les prochains etats à partir d'un etat donne
    def get_next_states(self, root):
        prequeued = {}
        queued = {}

    # calculer les etats  à passer  avec p max passagers pour aller sur le côte droit
    # prendre 0 à p missionnaires dans la barque
        for M in range(self.maxp_boats+1):

            # si le nombre de missionnaires n'est pas suffisant sur le côte gauche => inutile d'aller plus loin
            if (M > root.M_g):
                break

            # remplir la barque de 0 à p cannibales du côte droit
            for C in range(self.maxp_boats+1):
                # si personne ne revient de l'autre côte, il n'est pas necessaire d'aller plus loin, sauf si l'etat final est atteint.
                if (M == 0 and C == 0 and (root.M_g != 0 or root.C_g != 0)):
                    continue

                # si le nombre de cannibales n'est pas suffisant, pas besoin d'aller plus loin
                if (C > root.C_g):
                    break

                # verifier que l'on a suffisamment de place sur la barque
                if ((M+C) > self.maxp_boats):
                    break

                # creer un nouvel etat quand la barque est sur le côte droite
                node = Node(root.C_g-C, root.M_g-M, root.C_d+C, root.M_d+M)
                node.toRight = f'--> M:{M} C:{C}'

                # si l'etat n'est pas valide, pas besoin d'aller plus loin
                if node.is_valid() != True:
                    continue

                # si l'etat n'est pas dejà enregistre, on le met dans la liste d'attente
                if node not in prequeued:
                    prequeued[node] = node

        # calcule les etats à passer en retournant de nouveau sur le côte gauche.
        for node in prequeued:
            for M in range(self.maxp_boats+1):
                if (M > node.M_d):
                    break

                for C in range(self.maxp_boats+1):
                    if (M == 0 and C == 0 and (node.M_g != 0 or node.C_g != 0)):
                        continue
                    if (C > node.C_d):
                        break
                    if ((node.C_d-C) == 0 and (node.M_d-M) == 0):
                        continue
                    if ((M+C) > self.maxp_boats):
                        break
                    newNode = Node(node.C_g+C, node.M_g+M,
                                   node.C_d-C, node.M_d-M)
                    newNode.toRight = node.toRight
                    newNode.toLeft = f'<-- M:{M} C:{C}'

                    if newNode.is_valid() != True:
                        continue

                    if newNode not in queued:
                        queued[newNode] = newNode

        # les etats enregistres sont ajoutes dans le tableau states

        return queued.values()

    def bfs(self):
        self.queued.clear()
        self.visited.clear()
        self.parent.clear()

        self.queued = deque([self.start])  # on part du noeud initial
        self.parent = {self.start: None}  # on le reference sans parent

        while self.queued:
            state = self.queued.popleft()
            self.visited[state] = state
            if state == self.end:
                # pour mettre à jour les deplacements
                self.end = state
                return self.end

            for next_state in graph.get_next_states(state):
                if next_state not in self.visited:
                    self.visited[next_state] = next_state
                    self.parent[next_state] = state
                    self.queued.append(next_state)
        return None

    def get_solution(self):
        solutions = []
        parent = self.end

        while parent:  # tant que parent!=None
            solutions.append(parent)
            parent = self.parent[parent]

        solutions.reverse()
        return solutions


n = 5
root = Node(n, n, 0, 0)
end_root = Node(0, 0, n, n)
graph = Graph(root, end_root, 3)

start = time.time()

if graph.bfs():
    solutions = graph.get_solution()
    print("Solution:")
    for solution in solutions:
        print(solution.toRight)
        print(solution.toLeft)
        print('---')
        print(solution)
    print(f'Nombre detats visites: {len(graph.visited)}')
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'execution : {elapsed:.2}ms')
else:
    print("Pas de solution trouvee")
