# Algoritmo Animado Gift Wrapping
# Itzel Berenice Martínez Palacios
# Tarea 1

points = [] # Vector para guardar los puntos que se dibujan con el mouse
convex_hull = [] # Vector que guarda los puntos de la envoltura convexa

# ---------------------- VARIABLES PARA LA ANIMACIÓN ------------------------
is_calculating = False
left_most = -1 # idx del punto más a la izquierda
current_point_index = -1 # idx del punto actual
bestpoint_index = -1 # idx del mejor punto (hasta el momento)
to_check_point = 0 #idx del punto a checar

# Función base de Processing para modificar el lienzo de animación
def setup():
    fullScreen();
    background(255, 209, 220)
    frameRate(4) # frames por segundo de la animación
    
# Función que dibuja todo lo que le digamos (se ejecuta continuamente)
def draw():
    background(255, 209, 220)
    
    # Texto Gift Wrapping
    fill(0) # Color del texto (negro)
    textSize(70) # Tamaño de la fuente
    textAlign(CENTER)
    text("Gift Wrapping:", width / 2, 100) 
    
    # Dibuja todos los puntos y la envoltura (que se va construyendo)
    draw_points()
    draw_convex_hull()

    # Si la animación está activa, ejecuta un paso y dibuja las líneas
    if is_calculating:
        steps_giftWrapping() # Ejecuta el algoritmo paso por paso
        draw_steps_GiftWrapping_() # Dibuja el paso recién hecho

# -------------------- FUNCIONES BÁSICAS GEOMETRÍA ------------------------

EPS = 1e-9 # Epsilon pequeño por utilizar flotantes

# Producto cruz de los vectores: (p1 -> p2) x (p1 -> p3)
def cross_product(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

# Regresa true si el punto r está al lado izquierdo de la línea pq
def ccw(p, q, r):
    return cross_product(p, q, r) > EPS

# Regresa la norma euclideana de un vector
def norm(x, y):
    return float(x*x + y*y)


# ---------------- FUNCIONES INTERACTIVAS CON EL USUARIO ------------------

# Función para guardar los puntos que se van dibujando
def mousePressed():
    global is_calculating # Le indica a la función que la variable es global
    if mouseButton == LEFT:
        # Al añadir un punto detenemos la animación para iniciar de cero
        is_calculating = False
        points.append(PVector(mouseX, mouseY))
        
# Función que identifica lo ingresado por el usuario
def keyPressed():
    global is_calculating, points, convex_hull # Indica las variables como globales
    # Al presionar Enter se inicia la animación del Gift Wrapping
    if key == ENTER:
        start_calculation()
    # Al presionar "b", se borra todo en el lienzo
    if key == 'b':
        is_calculating = False
        points = [] # Reiniciamos el vector de puntos
        convex_hull = [] # Reiniciamos el vector de la envolvente convexa
        
# ------------------------ ALGORITMO Y ANIMACIÓN -----------------------

# Función para iniciar la búsqueda de la envolvente convexa
def start_calculation():
    global is_calculating, convex_hull, to_check_point, left_most, current_point_index, bestpoint_index

    # Con 3 puntos o menos, el convex hull es él mismo
    if len(points) < 3:
        convex_hull.extend(points)
        return

    # Reinicia las variables
    is_calculating = True
    convex_hull = []
    to_check_point = 0

    # Encuentra el punto más a la izquierda por coordenada (x) y en caso de empate (y)
    left_most = 0
    for i in range(1, len(points)):
        if points[i].x < points[left_most].x or (points[i].x == points[left_most].x and points[i].y < points[left_most].y):
            left_most = i # left_most es el elemento más a la izquierda
    
    current_point_index = left_most
    convex_hull.append(points[current_point_index]) # Sabemos que este punto está en la envolvente, así que lo agregamos.
    
    n = len(points)
    # Candidato inicial para el siguiente punto (siguiente punto en el vector de puntos)
    bestpoint_index = (current_point_index + 1) % n

# Búsqueda de la envolvente convexa
def steps_giftWrapping():
    global to_check_point, bestpoint_index, current_point_index, is_calculating
    
    # Compara el punto actual "to_check_point" con el mejor punto hasta ahora "bestpoint_index"
    orientation = cross_product(points[current_point_index], points[bestpoint_index], points[to_check_point])
    if orientation > EPS:
        bestpoint_index = to_check_point  # "to_check_point" es un mejor candidato
    elif abs(orientation) < EPS: # Si son colineales
        dist_to_endpoint = norm(points[current_point_index].x - points[bestpoint_index].x, points[current_point_index].y - points[bestpoint_index].y)
        dist_to_i = norm(points[current_point_index].x - points[to_check_point].x, points[current_point_index].y - points[to_check_point].y)
        if dist_to_i > dist_to_endpoint:
            bestpoint_index = to_check_point  # El punto más lejano es mejor

    to_check_point += 1

    # Si ya hicimos este proceso para todos los puntos
    if to_check_point >= len(points):
        # Si el siguiente punto es el punto con el que iniciamos, paramos
        if bestpoint_index == left_most:
            is_calculating = False
            return
        
        # Si no lo es, lo añadimos y volvemos a buscar
        current_point_index = bestpoint_index
        convex_hull.append(points[current_point_index])
        
        # Reiniciamos la búsqueda desde este nuevo punto
        to_check_point = 0
        bestpoint_index = (current_point_index + 1) % len(points)

# ---------------------- FUNCIONES DE DIBUJO ----------------------------

# Dibuja los puntos
def draw_points():
    for p in points:
        stroke(92, 9, 81)
        fill(158, 24, 140)
        ellipse(p.x, p.y, 15, 15)

# Dibuja el convex hull
def draw_convex_hull():
    if len(convex_hull) > 1:
        noFill()
        stroke(128, 23, 53)
        strokeWeight(5)
        beginShape()
        for p in convex_hull:
            vertex(p.x, p.y)
        if not is_calculating:
            endShape(CLOSE)
        else:
            endShape()

# Dibuja los pasos del algorirtmo
def draw_steps_GiftWrapping_():
    if current_point_index < 0 or bestpoint_index < 0 or to_check_point >= len(points):
        return

    current = points[current_point_index]
    endpoint = points[bestpoint_index]
    check = points[to_check_point]
    
    stroke(4, 145, 110)
    strokeWeight(4)
    line(current.x, current.y, endpoint.x, endpoint.y)
    
    stroke(105, 105, 105, 180)
    strokeWeight(3)
    line(current.x, current.y, check.x, check.y)
    
    # punto actual (azul)
    noFill()
    stroke(0, 0, 255)
    ellipse(current.x, current.y, 30, 30)
    
    # mejor punto hasta el momento (rojo)
    stroke(255, 0, 0)
    ellipse(endpoint.x, endpoint.y, 30, 30)
    
    # punto a checar (verde)
    stroke(0, 255, 0)
    ellipse(check.x, check.y, 30, 30)
