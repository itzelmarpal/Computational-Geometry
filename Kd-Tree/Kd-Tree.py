import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math


'''
    Geometría Computacional
    Itzel Berenice Martínez Palacios
    Proyecto Final
    Kd-Tree Vecino más cercano
'''
# ------------------- CONSTRUCCIÓN DE CLASES -------------------

# Clase de un Nodo para el Kd-Tree
class Node:
    def __init__(self, point, axis, left_child = None, right_child = None):
        self.point = point
        self.axis = axis # Guarda (0 -> X) y (1 -> Y)
        self.left_child = left_child
        self.right_child = right_child

# Estructura del Kd-Tree (inicialización y construcción)
class Kd_Tree:
    # Inicializacion de un kd-Tree
    def __init__(self, points):
        self.root = self.construction(points, 0)

    # Construcción del Kd-Tree 
    def construction(self, points, depth):
        # Casos Triviales
        if len(points) == 0:
            return None
        
        # Se define el eje actual
        curr_axis = depth % 2
        points.sort(key = lambda x: x[curr_axis])
        mid_idx = len(points) // 2

        # Recursivamente construimos el subárbol izquierdo y derecho
        # del punto medio respecto al eje actual
        mid_point = Node(
            point = points[mid_idx],
            axis = curr_axis,
            left_child = self.construction(points[:mid_idx], depth + 1),
            right_child= self.construction(points[mid_idx+1:], depth + 1)
        )
        return mid_point
    
    # Devuelve el punto más cercano a un punto dado de forma eficiente
    def closest_neighbour(self, point):
        return self.search_node(self.root, point, None, float('inf'))
    
    def search_node(self, init_point, goal_point, best_point, best_dist):
        if init_point == None:
            return best_point, best_dist
        
        # Calculamos la distancia del nodo meta al inicial
        dist = (goal_point[1] - init_point.point[1])**2 +\
                          (goal_point[0] - init_point.point[0])**2
        # Ahora comparamos y vemos si es el mejor punto hasta ahora
        if dist < best_dist:
            best_dist = dist
            best_point = init_point
        
        # Obtenemos el lado del árbol en el que está el punto meta
        diff = goal_point[init_point.axis] - init_point.point[init_point.axis]

        # Denotamos a las ramas del punto actual como rama cercana
        # y rama lejana en base a la variable 'diff'
        if diff < 0:
            close, away = (init_point.left_child, init_point.right_child) 
        else:
            close, away = (init_point.right_child, init_point.left_child)
        
        # Exploramos el árbol guiándonos por la rama más cercana
        best_point, best_dist = self.search_node(close, goal_point, best_point, best_dist)

        # Si el círculo de mejor radio cruza el plano de división cruzamos también al otro lado
        if diff**2 < best_dist:
            best_point, best_dist = self.search_node(away, goal_point, best_point, best_dist)
        
        return best_point, best_dist

# -------------------- ANIMACIÓN ------------------------

NO_POINTS = random.randint(10, 100)
LIM = 80
pos_mouse = [LIM/2, LIM/2]

# Generamos puntos aleatorios por todo el plano
points = [[np.random.uniform(0, LIM), np.random.uniform(0, LIM)] for _ in range(NO_POINTS)]

fig, ax = plt.subplots(figsize = (6, 6))
ax.set_xlim(0, LIM)
ax.set_ylim(0, LIM)
ax.set_title('Kd-Tree: Búsqueda del vecino más cercano')

# Inicialización de puntos en el plano
scatter_points = ax.scatter([], [], c = "#338fda", s = 50, alpha = 1 , label = 'Puntos Iniciales')
scatter_mouse = ax.scatter([], [], c = "#ffaa00", s = 200, marker = '*', alpha = 1, label = 'Punto de interés')
scatter_neighbour = ax.scatter([], [], c = "#e74757", s = 200, marker = 'x', alpha = 1, label = 'Vecino más cercano')
conection_lines, = ax.plot([], [], 'm--', alpha = 0.5)
tree_lines = []

# Función para graficar el algoritmo
def draw_tree_lines(node, min_x, min_y, max_x, max_y):
    if node is None:
        return

    if node.axis == 0: # Corte respecto al eje X (HORIZONTAL)
        line, = ax.plot([node.point[0], node.point[0]], [min_y, max_y], 'k-', alpha = 0.2)
        tree_lines.append(line)
        draw_tree_lines(node.left_child, min_x, min_y, node.point[0], max_y)
        draw_tree_lines(node.right_child, node.point[0], min_y, max_x, max_y)
    else: # Corte respecto al eje Y (VERTICAL)
        line, = ax.plot([min_x, max_x], [node.point[1], node.point[1]], 'k-', alpha = 0.2)
        tree_lines.append(line)
        draw_tree_lines(node.left_child, min_x, min_y, max_x, node.point[1])
        draw_tree_lines(node.right_child, min_x, node.point[1], max_x, max_y)

# Captura el movimiento del mouse
def mouse_capture(event):
    if event.xdata and event.ydata:
        pos_mouse[0] = event.xdata
        pos_mouse[1] = event.ydata

# Elegimos que accione cuando el mouse se presione (o cuando el mouse se mueva)
fig.canvas.mpl_connect('button_press_event', mouse_capture)
#fig.canvas.mpl_connect('motion_notify_event', mouse_capture)

# Inicializamos el Kd-Tree con los puntos generados
tree = Kd_Tree(points.copy())
draw_tree_lines(tree.root, 0, 0, LIM, LIM)
scatter_points.set_offsets(points)

# Función que actualiza la posición más cercana
def update_search(frame):    
    neighbour, dist = tree.closest_neighbour(pos_mouse)

    scatter_mouse.set_offsets([pos_mouse])
    if neighbour:
        scatter_neighbour.set_offsets([neighbour.point])
        conection_lines.set_data([pos_mouse[0], neighbour.point[0]], [pos_mouse[1], neighbour.point[1]])
    return scatter_points, scatter_neighbour, scatter_mouse, conection_lines

# Realizamos la animación
animation_kdTree = animation.FuncAnimation(fig, update_search, frames = 200, interval = 50, blit = False)
plt.legend(loc ='upper right')
plt.show()