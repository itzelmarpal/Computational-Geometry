# Algoritmo Animado Graham Scan
# Itzel Berenice Martínez Palacios
# Tarea 1

import math
from functools import cmp_to_key

# --- VARIABLES GLOBALES ---
points = [] # Vector para guardar los puntos que se dibujan con el mouse
convex_hull = [] # Funciona como el stack del Graham Scan
polarAngle_sorted = [] # Guarda los puntos ordenados respecto al ángulo polar
m = 0 # Guarda el número de puntos sin contar los colineales

# --- VARIABLES PARA LA ANIMACIÓN ---
is_calculating = False
current_point_index = 0 # Índice para el punto actual en el cálculo
pivot_point = None # Punto con coordenada y menor.

# Función base de Processing para modificar el lienzo de animación
def setup():
    fullScreen()
    background(232, 180, 125)
    frameRate(2) # frames por segundo de la animación

# Función que va dibujando en pantalla (se ejecuta continuamente)
def draw():
    background(232, 180, 125)
    
    # Texto Graham Scan
    fill(0)
    textSize(70)
    textAlign(CENTER)
    text("Graham Scan", width / 2, 100)
    
    # Si "is_calculating" es verdadero, realizamos un paso del algoritmo
    if is_calculating:
        steps_grahamScan() # Realiza un paso del algoritmo
        draw_steps_grahamScan() # Se dibuja el paso realizado
        
    draw_points() # Se dibujan los puntos originales
    draw_convex_hull() # Se dibuja la envolvente convexa actual

# -------------------- FUNCIONES BÁSICAS GEOMETRÍA ------------------------
EPS = 1e-9 # Epsilon pequeño para tratar flotantes 

# Función que nos ayuda a detectar si un giro es CCW o CW
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if abs(val) < EPS:
        return 0  # Colineal
    return 1 if val > 0 else -1  # 1 para CCW, -1 CW

# Distancia entre dos puntos al cuadrado
def distSq(p1, p2):
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2

# ---------------- FUNCIONES INTERACTIVAS CON EL USUARIO ------------------

# Detecta los clicks izquierdos y añade esos puntos al vector points
def mousePressed():
    global is_calculating, points, convex_hull, polarAngle_sorted
    if mouseButton == LEFT:
        is_calculating = False
        points.append(PVector(mouseX, mouseY))

# Detecta otras teclas del usuario    
def keyPressed():
    global is_calculating, points, convex_hull
    if key == ENTER: # Al presionar Enter, inicia el algoritmo
        if len(points) >= 3:
            start_calculation()
    if key == 'b': # Borra todo lo realizado anteriormente
        is_calculating = False
        points = []
        convex_hull = []

# --------------------------- ALGORITMO Y ANIMACIÓN -------------------------
# Prepara todo para ejecutar el algoritmo
def start_calculation():
    global is_calculating, convex_hull, pivot_point, polarAngle_sorted, m, current_point_index
    
    # Si solo tenemos dos puntos, no ocupamos calcular nada
    if len(points) < 3:
        return

    # Encuentra el punto pivote (con la coordenada y más baja). Desempata con la coordenada x
    min_idx = 0
    for i in range(1, len(points)):
        if (points[i].y < points[min_idx].y) or \
           (points[i].y == points[min_idx].y and points[i].x < points[min_idx].x):
            min_idx = i
    
    # Se intercambia el punto pivote, para que quede al inicio
    points[0], points[min_idx] = points[min_idx], points[0] # swap
    pivot_point = points[0]

    # Ordenamos los puntos por ángulo polar respecto al punto pivote
    def compare(p1, p2):
        o = orientation(pivot_point, p1, p2)
        if abs(o) < EPS: # Si son colineales, el más cercano va primero
            return -1 if distSq(pivot_point, p1) < distSq(pivot_point, p2) else 1
        return -o # CCW

    # Ordenamos todos los puntos menos el pivote
    sorted_points = sorted(points[1:], key=cmp_to_key(compare)) # Se ordena el vector
    # Guardamos los puntos ordenados respecto al ángulo polar del pivote
    polarAngle_sorted = [pivot_point] + sorted_points

    # Se eliminan los puntos colineales intermedios
    m = 1
    for i in range(1, len(polarAngle_sorted)):
        # Mientras el punto siguiente es colineal, lo ignoramos
        while i < len(polarAngle_sorted) - 1 and \
              abs(orientation(pivot_point, polarAngle_sorted[i], polarAngle_sorted[i+1])) < EPS:
            i += 1
        # De los puntos colineales guardamos el más lejano
        polarAngle_sorted[m] = polarAngle_sorted[i]
        m += 1
    
    # Reducimos el vector únicamente a los puntos que nos importan
    polarAngle_sorted = polarAngle_sorted[:m]
    
    # Si después de esto nos quedan solo 3 puntos, no ocupamos hacer nada más
    if m < 3:
        is_calculating = False
        convex_hull = polarAngle_sorted
        return
    # Indicamos que vamos a iniciar la animación
    is_calculating = True
    convex_hull = [polarAngle_sorted[0], polarAngle_sorted[1]]
    current_point_index = 2

# Búsqueda de la envolvente convexa
def steps_grahamScan():
    global current_point_index, is_calculating, convex_hull
    
    # Si ya pasamos por todos los puntos, terminamos.
    if current_point_index >= m:
        is_calculating = False
        return
        
    # Regresamos si solo tenemos un punto (ya que ocupamos 2)
    if len(convex_hull) < 2:
        is_calculating = False
        return
        
    # Tomamos a los últimos dos puntos del stack p1, y p2
    p1 = convex_hull[-2]
    p2 = convex_hull[-1]
    point_to_check = polarAngle_sorted[current_point_index] # Punto candidato
    
    # Si no es counter-clockwise
    if orientation(p1, p2, point_to_check) != 1:
        convex_hull.pop() # Quitamos el último punto del stack.
    else: # Si es counter-clockwise
        convex_hull.append(point_to_check) # Se agrega el punto candidato
        current_point_index += 1 # Pasamos al próximo punto

# ------------------ FUNCIONES DE DIBUJO ------------------

# Se dibujan todos los puntos añadidos
def draw_points():
    for p in points:
        stroke(117, 74, 34)
        fill(204, 122, 45)
        ellipse(p.x, p.y, 15, 15)

# Se dibuja la envolvente convexa actual
def draw_convex_hull():
    if len(convex_hull) > 1:
        noFill()
        stroke(66, 21, 171)
        strokeWeight(4)
        beginShape()
        for p in convex_hull:
            vertex(p.x, p.y)
        # Si ya no se está calculando, cerramos el polígono
        if not is_calculating and len(convex_hull) > 2:
            endShape(CLOSE)
        else:
            endShape()
    # Si solo tenemos dos puntos, se dibuja una línea
    elif not is_calculating and len(points) == 2:
        stroke(128, 23, 53)
        strokeWeight(4)     # Mismo grosor
        line(points[0].x, points[0].y, points[1].x, points[1].y)

# Se dibuja el paso a paso del algoritmo
def draw_steps_grahamScan():
    # Si no está activo el algoritmo o tenemos un solo punto, no dibujamos nada
    if not is_calculating or len(convex_hull) < 2 or current_point_index >= m:
        return
    
    # Los puntos que tratamos en el algoritmo
    p1 = convex_hull[-2]
    p2 = convex_hull[-1]
    p3 = polarAngle_sorted[current_point_index]
    
    noFill()
    strokeWeight(3)
    
    # penúltimo punto del stack en azul
    stroke(0, 0, 255)
    ellipse(p1.x, p1.y, 30, 30)
    
    # último del stack en rojo
    stroke(255, 0, 0)
    ellipse(p2.x, p2.y, 30, 30)
    
    # punto candidato en verde
    stroke(0, 255, 0)
    ellipse(p3.x, p3.y, 30, 30)
