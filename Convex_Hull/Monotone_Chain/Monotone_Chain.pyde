# Algoritmo Animado Monotone Chain
# Itzel Berenice Martínez Palacios
# Tarea 1

import math
from functools import cmp_to_key

# --- VARIABLES GLOBALES ---
points = [] # Vector para guardar los puntos que se dibujan con el mouse 
sorted_points = []# Vector para guardar los puntos ordenados
convex_hull = [] # Vector que guarda los puntos de la envoltura convexa
U = [] # Cubierta superior
L = [] # Cubierta inferior

# --- VARIABLES PARA LA ANIMACIÓN ---
is_calculating = False
current_point_idx = 0
LOW_or_UP = "LOW" # Indicador de en qué etapa estamos

# Función base de Processing para modificar el lienzo de animación
def setup():
    fullScreen()
    background(122, 193, 255)
    frameRate(2)  # frames por segundo de la animación

# Función base de Processing para modificar el lienzo de animación
def draw():
    background(122, 193, 255)
    
    # Texto
    fill(0)
    textSize(70)
    textAlign(CENTER)
    text("Monotone Chain", width / 2, 100)
    
    # Si la animación está activa, ejecuta un paso y dibuja las líneas
    if is_calculating:
        steps_monotone_Chain() # Ejecuta el algoritmo paso por paso
        draw_steps_monotoneChain() # Dibuja el paso recién hecho
        
    # Dibuja todos los puntos y la envoltura (que se va construyendo)
    draw_points()
    draw_convex_hull()

# -------------------- FUNCIONES BÁSICAS GEOMETRÍA ------------------------
EPS = 1e-9

# Determina la orientación de tres puntos (p, q, r). 
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if abs(val) < EPS: # Colineales
        return 0
    return 1 if val > EPS else -1 # CCW o CW

# ---------------- FUNCIONES INTERACTIVAS CON EL USUARIO ------------------
# Función para guardar los puntos que se van dibujando
def mousePressed():
    global is_calculating, points
    if mouseButton == LEFT:
        # Al añadir un punto detenemos la animación para iniciar de cero
        is_calculating = False
        points.append(PVector(mouseX, mouseY))

# Función que identifica lo ingresado por el usuario        
def keyPressed():
    global is_calculating, points, convex_hull, U, L
    # Al presionar Enter se inicia la animación del Monotone_Chain
    if key == ENTER:
        if len(points) >= 3:
            start_calculation()
    # Al presionar "b", se borra todo en el lienzo
    if key == 'b' or key == 'B':
        is_calculating = False
        points = []  # Reiniciamos el vector de puntos
        convex_hull = [] # Reiniciamos el vector de la envolvente convexa
        L = [] # Reiniciamos L
        U = [] # Reiniciamos U

# --------------------------- ALGORITMO Y ANIMACIÓN -------------------------
# Prepara e inicializa todas las variables para comenzar el cálculo del algoritmo
def start_calculation():
    global is_calculating, sorted_points, points, convex_hull, U, L, current_point_idx, LOW_or_UP
    
    # Si no hay al menos tres puntos, se regresa.
    if len(points) < 3:
        is_calculating = False
        convex_hull = list(points)
        return
    
    # Limpia las listas de resultados anteriores.
    L, U, convex_hull = [], [], []
    
    # Ordena los puntos lexicográficamente 
    sorted_points = sorted(points, key=lambda p: (p.x, p.y))
    
    # Inicia la animación.
    is_calculating = True
    LOW_or_UP = "LOW"
    current_point_idx = 0

# Realiza paso a paso el algoritmo Monotone Chain
def steps_monotone_Chain():  
    global is_calculating, sorted_points, convex_hull, U, L, current_point_idx, LOW_or_UP  
    
    # Construcción de la cubierta inferior
    if LOW_or_UP == "LOW":
        if current_point_idx >= len(sorted_points):
            LOW_or_UP = "UP"
            current_point_idx = len(sorted_points) - 1
            return
        p = sorted_points[current_point_idx]
        
        if len(L) >= 2 and orientation(L[-2], L[-1], p) <= 0:
            L.pop()
        else:
            L.append(p)
            current_point_idx += 1
    # Construcción de la cubierta superior
    elif LOW_or_UP == "UP":
        if current_point_idx < 0:
            LOW_or_UP = "DONE"
            return
        p = sorted_points[current_point_idx]
        
        if len(U) >= 2 and orientation(U[-2], U[-1], p) <= 0:
            U.pop()
        else:
            U.append(p)
            current_point_idx -= 1
            
    elif LOW_or_UP == "DONE":
        convex_hull = L[:-1] + U[:-1]
        is_calculating = False
        
# ------------------ FUNCIONES DE DIBUJO ------------------
# Dibuja los puntos
def draw_points():
    for p in points:
        stroke(117, 74, 34)
        fill(204, 122, 45)
        ellipse(p.x, p.y, 15, 15)

# Dibuja el convex hull
def draw_convex_hull():
    noFill()
    strokeWeight(5)
    
    if is_calculating:
        stroke(200, 0, 0) # Rojo
        beginShape()
        for p in L:
            vertex(p.x, p.y)
        endShape()
        
        stroke(0, 150, 0) # Verde
        beginShape()
        for p in U:
            vertex(p.x, p.y)
        endShape()
        
    elif convex_hull:
        stroke(255, 100, 0) # Naranja
        beginShape()
        for p in convex_hull:
            vertex(p.x, p.y)
        endShape(CLOSE)

# Dibuja los pasos del algorirtmo
def draw_steps_monotoneChain():
    if LOW_or_UP == "DONE" or (LOW_or_UP == "LOW" and current_point_idx >= len(sorted_points)) or \
       (LOW_or_UP == "UP" and current_point_idx < 0):
        return

    noFill()
    strokeWeight(3)

    p_check = sorted_points[current_point_idx]
    stroke(38, 135, 38) # Verde
    ellipse(p_check.x, p_check.y, 40, 40)

    active_stack = L if LOW_or_UP == "LOW" else U
    
    if len(active_stack) >= 2:
        p1 = active_stack[-2]
        stroke(0, 0, 255) # Azul
        ellipse(p1.x, p1.y, 40, 40)

        p2 = active_stack[-1]
        stroke(255, 0, 0) # Rojo
        ellipse(p2.x, p2.y, 40, 40)
