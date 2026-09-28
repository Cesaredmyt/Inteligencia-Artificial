"""
A* "Evaluación Asterisco"
--------------------------------------------------------
Materia: Inteligencia Artificial
Alumno : Cesar Enrique Diaz Maldonado

Reglas:
  - La búsqueda parte de la SALIDA y termina en el INICIO
    (por eso la Lista Cerrada empieza con la SALIDA).
  - Movimiento en 8 direcciones: recto = 10, diagonal = 14.
  - h(n) = distancia Manhattan * 10 hacia el objetivo.
  - f(n) = g(n) + h(n).
  - Se expande el nodo de La con menor f. Si hay empate, el que entró primero.
  - Cada celda muestra su número, g, h, f y una flecha roja hacia su PADRE.
  - Azul = ya está en la Lista Cerrada (Lc). Gris = pared.

Controles:
    ESPACIO / FLECHA DERECHA -> siguiente paso
    FLECHA IZQUIERDA         -> paso anterior
    A                        -> avance automático (on/off)
    F                        -> ir al final
    R                        -> reiniciar
    E                        -> modo editar paredes (clic para poner/quitar)
    S + clic (en modo editar)-> mover SALIDA
    I + clic (en modo editar)-> mover INICIO
    D                        -> cargar el tablero de ejemplo (7x9)
    Q / ESC                  -> salir
"""

import math
import pygame

# ----------------------------------------------------------------------
# 1. ALGORITMO A*
# ----------------------------------------------------------------------

FILAS_DEF, COLS_DEF = 7, 9
COSTO_RECTO, COSTO_DIAG = 10, 14

# Orden en que se generan los vecinos (de abajo hacia arriba). Este orden
# es el que reproduce el desempate del ejercicio en Excel.
ORDEN_VECINOS = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]


def num(r, c, cols):
    return r * cols + c + 1


def pos(n, cols):
    return ((n - 1) // cols, (n - 1) % cols)


def manhattan10(a, b, cols):
    """h(a -> b) = (|dFilas| + |dColumnas|) * 10.
    Solo cuenta pasos rectos (vertical/horizontal) y NO mira las paredes."""
    ra, ca = pos(a, cols)
    rb, cb = pos(b, cols)
    return (abs(ra - rb) + abs(ca - cb)) * 10


def astar_pasos(filas, cols, paredes, salida, inicio):
    """
    Corre A* de `salida` hacia `inicio` y devuelve una lista de pasos.
    Cada paso es un dict con el estado COMPLETO en ese momento, para poder
    avanzar y retroceder sin recalcular.
    """
    g = {salida: 0}
    padre = {}
    La = [salida]              # lista abierta (en orden de llegada)
    Lc = []                    # lista cerrada (en orden de expansión)
    llegada = {salida: 0}
    contador = 1
    pasos = []

    def foto(actual, nuevos, mensaje):
        pasos.append({
            "actual": actual,
            "nuevos": list(nuevos),
            "g": dict(g),
            "padre": dict(padre),
            "La": sorted(La, key=lambda n: (g[n] + manhattan10(n, inicio, cols), llegada[n])),
            "Lc": list(Lc),
            "mensaje": mensaje,
        })

    foto(None, [], f"Inicio: La = [{salida}]  (SALIDA, g=0)")

    while La:
        actual = min(La, key=lambda n: (g[n] + manhattan10(n, inicio, cols), llegada[n]))
        La.remove(actual)
        Lc.append(actual)

        if actual == inicio:
            foto(actual, [], f"Se expande {actual} = INICIO  ->  ¡camino encontrado! costo g = {g[actual]}")
            return pasos, True

        r, c = pos(actual, cols)
        nuevos = []
        for dr, dc in ORDEN_VECINOS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < filas and 0 <= nc < cols):
                continue
            v = num(nr, nc, cols)
            if v in paredes or v in Lc:
                continue
            costo = COSTO_DIAG if (dr and dc) else COSTO_RECTO
            ng = g[actual] + costo
            if v not in g or ng < g[v]:
                g[v] = ng
                padre[v] = actual
                if v not in La:
                    La.append(v)
                llegada[v] = contador
                contador += 1
                nuevos.append(v)

        f_act = g[actual] + manhattan10(actual, inicio, cols)
        foto(actual, nuevos,
             f"Se expande {actual} (g={g[actual]}, h={manhattan10(actual, inicio, cols)}, f={f_act}) "
             f"-> Lc; nuevos/actualizados en La: {nuevos if nuevos else 'ninguno'}")

    foto(None, [], "La quedó vacía: NO hay camino")
    return pasos, False


def reconstruir_camino(padre, inicio, salida):
    camino = [inicio]
    while camino[-1] != salida:
        if camino[-1] not in padre:
            return []
        camino.append(padre[camino[-1]])
    return camino


# ----------------------------------------------------------------------
# 2. TABLERO DE EJEMPLO
# ----------------------------------------------------------------------

EJEMPLO = {
    "filas": 7, "cols": 9,
    "paredes": {12, 16, 21, 25, 30, 34, 39, 40, 41, 42, 43},
    "salida": 5, "inicio": 59,
}

# ----------------------------------------------------------------------
# 3. INTERFAZ PYGAME
# ----------------------------------------------------------------------

CELDA_W_BASE, CELDA_H_BASE = 92, 78
MAX_FILAS, MAX_COLS = 30, 40
PANEL_DER = 330
ALTO_SUP = 64
ALTO_INF = 96

C_FONDO = (255, 255, 255)
C_LINEA = (140, 140, 140)
C_AZUL = (220, 230, 241)
C_PARED = (217, 217, 217)
C_SALIDA = (146, 208, 80)
C_INICIO = (255, 192, 0)
C_ACTUAL = (255, 245, 157)
C_NUEVO = (255, 224, 178)
C_TEXTO = (20, 20, 20)
C_ROJO = (220, 20, 20)
C_CAMINO = (0, 130, 60)
C_BARRA = (30, 30, 30)


def dibujar_flecha(pantalla, p_ini, p_fin, color=C_ROJO, grosor=2):
    """Flecha desde p_ini hacia p_fin (con punta triangular)."""
    pygame.draw.line(pantalla, color, p_ini, p_fin, grosor)
    ang = math.atan2(p_fin[1] - p_ini[1], p_fin[0] - p_ini[0])
    largo = max(4, min(9, math.hypot(p_fin[0] - p_ini[0], p_fin[1] - p_ini[1]) * 0.6))
    for delta in (math.radians(155), math.radians(-155)):
        x = p_fin[0] + largo * math.cos(ang + delta)
        y = p_fin[1] + largo * math.sin(ang + delta)
        pygame.draw.line(pantalla, color, p_fin, (x, y), grosor)


class App:
    def __init__(self):
        pygame.init()
        self.fuente = pygame.font.SysFont("Arial", 15)
        self.fuente_b = pygame.font.SysFont("Arial", 15, bold=True)
        self.fuente_p = pygame.font.SysFont("Arial", 13)
        self.fuente_t = pygame.font.SysFont("Arial", 20, bold=True)
        self.reloj = pygame.time.Clock()
        self.auto = False
        self.ultimo_auto = 0
        self.editar = False
        self.cargar(EJEMPLO)

    # ---- estado del tablero ----
    def cargar(self, cfg):
        self.filas, self.cols = cfg["filas"], cfg["cols"]
        self.paredes = set(cfg["paredes"])
        self.salida, self.inicio = cfg["salida"], cfg["inicio"]
        self.crear_ventana()
        self.reiniciar()

    def crear_ventana(self):
        """Ajusta el tamaño de celda para que todo quepa en la pantalla."""
        info = pygame.display.Info()
        max_w = max(800, info.current_w - 60)
        max_h = max(600, info.current_h - 120)
        # tamaño ideal, y se reduce si no cabe
        # El panel derecho se encoge si la pantalla es angosta
        panel = PANEL_DER if max_w >= 1100 else 250
        k = min(1.0,
                (max_w - panel) / (self.cols * CELDA_W_BASE),
                (max_h - ALTO_SUP - ALTO_INF) / (self.filas * CELDA_H_BASE))
        # Mínimo absoluto legible por debajo de esto
        # el tablero simplemente se dibuja más chico, pero SIEMPRE cabe en pantalla.
        self.celda_w = max(14, int(CELDA_W_BASE * k))
        self.celda_h = max(12, int(CELDA_H_BASE * k))
        # celdas chicas: solo número y f
        # Se muestran g, h y f completos mientras quepan 4 líneas con letra legible
        self.compacto = self.celda_h < 4 * 11 + 6
        # Fuentes de la interfaz: SIEMPRE legibles, tamaño fijo
        self.fuente = pygame.font.SysFont("Arial", 15)
        self.fuente_b = pygame.font.SysFont("Arial", 15, bold=True)
        self.fuente_p = pygame.font.SysFont("Arial", 13)
        # Fuentes de las celdas: escalan con el tamaño de celda
        tam = max(9, min(15, int((self.celda_h - 6) / 4.6)))
        self.f_celda = pygame.font.SysFont("Arial", tam)
        self.f_celda_b = pygame.font.SysFont("Arial", tam, bold=True)
        w = self.cols * self.celda_w + panel
        h = ALTO_SUP + self.filas * self.celda_h + ALTO_INF
        self.pantalla = pygame.display.set_mode((w, h))
        pygame.display.set_caption("A* — formato Evaluación Asterisco")

    def reiniciar(self):
        self.pasos, self.encontrado = astar_pasos(
            self.filas, self.cols, self.paredes, self.salida, self.inicio)
        self.i = 0
        self.auto = False

    def redimensionar(self, filas, cols):
        """Cambia el tamaño del tablero. Las paredes/salida/inicio se conservan si caben."""
        filas, cols = max(2, min(MAX_FILAS, filas)), max(2, min(MAX_COLS, cols))
        if (filas, cols) == (self.filas, self.cols):
            return
        # Se reubican las celdas por (fila, col) para no perder las paredes al cambiar el ancho
        def a_rc(n):
            return pos(n, self.cols)
        nuevas = set()
        for n in self.paredes:
            r, c = a_rc(n)
            if r < filas and c < cols:
                nuevas.add(num(r, c, cols))
        def reubicar(n, defecto):
            r, c = a_rc(n)
            return num(r, c, cols) if (r < filas and c < cols) else defecto
        salida = reubicar(self.salida, num(0, cols // 2, cols))
        inicio = reubicar(self.inicio, num(filas - 1, cols // 2, cols))
        if salida == inicio:
            inicio = num(filas - 1, 0, cols) if salida != num(filas - 1, 0, cols) else num(0, 0, cols)
        nuevas.discard(salida)
        nuevas.discard(inicio)
        self.filas, self.cols = filas, cols
        self.paredes, self.salida, self.inicio = nuevas, salida, inicio
        self.crear_ventana()
        self.reiniciar()

    def aleatorio(self, densidad=0.25):
        """Coloca paredes al azar (deja libres salida e inicio)."""
        import random
        total = self.filas * self.cols
        self.paredes = {n for n in range(1, total + 1)
                        if n not in (self.salida, self.inicio) and random.random() < densidad}
        self.reiniciar()

    # ---- geometría ----
    def rect_celda(self, n):
        r, c = pos(n, self.cols)
        return pygame.Rect(c * self.celda_w, ALTO_SUP + r * self.celda_h, self.celda_w, self.celda_h)

    def celda_en(self, p):
        x, y = p
        if y < ALTO_SUP:
            return None
        c, r = x // self.celda_w, (y - ALTO_SUP) // self.celda_h
        if 0 <= r < self.filas and 0 <= c < self.cols:
            return num(r, c, self.cols)
        return None

    def borde_hacia(self, n_desde, n_hasta):
        """Punto de salida/llegada de la flecha, cerca de los bordes de las celdas."""
        a = self.rect_celda(n_desde).center
        b = self.rect_celda(n_hasta).center
        dx, dy = b[0] - a[0], b[1] - a[1]
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx / dist, dy / dist
        # se acorta para que la flecha no tape los números
        if self.compacto:
            # Celda chica: la flecha va de borde a borde y NO invade el interior,
            # así no tapa el número ni el valor de f.
            kx, ky = self.celda_w * 0.46, self.celda_h * 0.46
        else:
            kx, ky = self.celda_w * 0.28, self.celda_h * 0.28
        ini = (a[0] + ux * kx, a[1] + uy * ky)
        fin = (b[0] - ux * kx, b[1] - uy * ky)
        return ini, fin

    # ---- dibujo ----
    def dibujar_celda(self, n, paso):
        rect = self.rect_celda(n)
        g = paso["g"]
        en_lc = n in paso["Lc"]

        if n in self.paredes:
            color = C_PARED
        elif n == self.salida:
            color = C_SALIDA
        elif n == self.inicio and en_lc:
            color = C_INICIO
        elif n == paso["actual"]:
            color = C_ACTUAL
        elif en_lc:
            color = C_AZUL
        elif n in paso["nuevos"]:
            color = C_NUEVO
        elif n == self.inicio:
            color = C_INICIO
        else:
            color = C_FONDO

        pygame.draw.rect(self.pantalla, color, rect)
        pygame.draw.rect(self.pantalla, C_LINEA, rect, 1)

        cx, cy = rect.centerx, rect.centery
        if n in self.paredes:
            if self.compacto:
                t = self.f_celda.render(f"{n}", True, (110, 110, 110))
                self.pantalla.blit(t, (cx - t.get_width() // 2, cy - t.get_height() // 2))
            else:
                t = self.f_celda.render(f"{n}", True, C_TEXTO)
                self.pantalla.blit(t, (cx - t.get_width() // 2, cy - 16))
                t = self.f_celda.render("(pared)", True, C_TEXTO)
                self.pantalla.blit(t, (cx - t.get_width() // 2, cy + 2))
            return

        etiqueta = str(n)
        if n == self.salida:
            etiqueta = f"{n} - SALIDA" if not self.compacto else f"{n} S"
        elif n == self.inicio:
            etiqueta = f"{n} - INICIO" if not self.compacto else f"{n} I"
        t = self.f_celda_b.render(etiqueta, True, C_TEXTO)

        if n in g:
            gv = g[n]
            hv = manhattan10(n, self.inicio, self.cols)
            lineas = [f"g={gv}", f"h={hv}", f"f={gv + hv}"]
        else:
            lineas = ["g=", "h=", "f="]

        if self.compacto:
            # celda chica: número arriba y solo f abajo (g y h en el panel al pasar el mouse)
            self.pantalla.blit(t, (cx - t.get_width() // 2, rect.y + 2))
            tf = self.f_celda.render(lineas[2], True, C_TEXTO)
            self.pantalla.blit(tf, (cx - tf.get_width() // 2, rect.bottom - tf.get_height() - 2))
        else:
            self.pantalla.blit(t, (cx - t.get_width() // 2, rect.y + 4))
            paso_y = self.f_celda.get_linesize()
            for k, txt in enumerate(lineas):
                tt = self.f_celda.render(txt, True, C_TEXTO)
                self.pantalla.blit(tt, (cx - tt.get_width() // 2, rect.y + 6 + t.get_height() + k * paso_y))

    def dibujar_flechas(self, paso):
        for hijo, padre in paso["padre"].items():
            if hijo in self.paredes:
                continue
            # La flecha va del HIJO hacia su PADRE
            ini, fin = self.borde_hacia(hijo, padre)
            dibujar_flecha(self.pantalla, ini, fin)

    def dibujar_camino(self, paso):
        if self.i != len(self.pasos) - 1 or not self.encontrado:
            return
        camino = reconstruir_camino(paso["padre"], self.inicio, self.salida)
        # Se resalta el borde de cada celda del camino
        for n in camino:
            pygame.draw.rect(self.pantalla, C_CAMINO, self.rect_celda(n), 4)

    def texto_lista(self, x, y, titulo, items, ancho, resaltar=None, max_lineas=9):
        t = self.fuente_b.render(titulo, True, C_TEXTO)
        self.pantalla.blit(t, (x, y))
        y += 22
        linea, lineas = "", []
        for k, it in enumerate(items):
            trozo = str(it) + (", " if k < len(items) - 1 else "")
            if self.fuente.size(linea + trozo)[0] > ancho:
                lineas.append(linea)
                linea = ""
            linea += trozo
        if linea:
            lineas.append(linea)
        for l in lineas[-max_lineas:]:
            t = self.fuente.render(l, True, C_TEXTO)
            self.pantalla.blit(t, (x, y))
            y += 18
        return y

    def dibujar_panel(self, paso):
        x0 = self.cols * self.celda_w + 14
        ancho = self.pantalla.get_width() - self.cols * self.celda_w - 28
        pygame.draw.rect(self.pantalla, (245, 245, 245),
                         (self.cols * self.celda_w, ALTO_SUP, self.pantalla.get_width() - self.cols * self.celda_w, self.filas * self.celda_h))
        y = ALTO_SUP + 8
        t = self.fuente_t.render(f"Paso {self.i} / {len(self.pasos) - 1}", True, C_TEXTO)
        self.pantalla.blit(t, (x0, y))
        y += 34

        La_txt = [f"{n}(f={paso['g'][n] + manhattan10(n, self.inicio, self.cols)})" for n in paso["La"]]
        y = self.texto_lista(x0, y, "Lista Abierta (La)  ordenada por f:", La_txt or ["vacía"], ancho, max_lineas=7)
        y += 10
        y = self.texto_lista(x0, y, "Lista Cerrada (Lc):", paso["Lc"] or ["vacía"], ancho, max_lineas=7)
        y += 10
        leyenda = [
            (C_ACTUAL, "nodo que se expande ahora"),
            (C_NUEVO, "nuevos / actualizados en La"),
            (C_AZUL, "ya en Lista Cerrada"),
            (C_PARED, "pared"),
        ]
        y_max = ALTO_SUP + self.filas * self.celda_h - 20
        for col, txt in leyenda:
            if y > y_max - 60:
                break
            pygame.draw.rect(self.pantalla, col, (x0, y, 16, 16))
            pygame.draw.rect(self.pantalla, C_LINEA, (x0, y, 16, 16), 1)
            t = self.fuente_p.render(txt, True, C_TEXTO)
            self.pantalla.blit(t, (x0 + 24, y))
            y += 21
        if y < y_max - 40:
            t = self.fuente_p.render("→ flecha roja: apunta al PADRE", True, C_ROJO)
            self.pantalla.blit(t, (x0, y + 2))
            pygame.draw.rect(self.pantalla, C_CAMINO, (x0, y + 26, 16, 16), 3)
            t = self.fuente_p.render("borde verde: camino final", True, C_CAMINO)
            self.pantalla.blit(t, (x0 + 24, y + 26))

    def dibujar_barras(self, paso):
        w = self.pantalla.get_width()
        pygame.draw.rect(self.pantalla, C_BARRA, (0, 0, w, ALTO_SUP))
        modo = "EDITAR: clic = pared | S+clic = salida | I+clic = inicio | E = salir de editar" if self.editar \
            else "ESPACIO/→ sig. | ← ant. | A auto | F final | R reinicia | E editar | D ejemplo"
        t = self.fuente.render(modo, True, (255, 255, 255))
        self.pantalla.blit(t, (10, 8))
        t = self.fuente_b.render(paso["mensaje"], True, (255, 230, 120))
        self.pantalla.blit(t, (10, 34))

        y0 = ALTO_SUP + self.filas * self.celda_h
        pygame.draw.rect(self.pantalla, (250, 250, 250), (0, y0, w, ALTO_INF))
        pygame.draw.line(self.pantalla, C_LINEA, (0, y0), (w, y0))
        self.pantalla.blit(self.fuente_p.render(
            "h = Manhattan x10 = (|dFilas| + |dColumnas|) x 10   |   recto = 10, diagonal = 14   |   f = g + h",
            True, (90, 90, 90)), (10, y0 + ALTO_INF - 22))
        if self.i == len(self.pasos) - 1:
            if self.encontrado:
                cam = reconstruir_camino(paso["padre"], self.inicio, self.salida)
                self.pantalla.blit(self.fuente_b.render(
                    f"Camino (INICIO → SALIDA): {' → '.join(map(str, cam))}", True, C_CAMINO), (10, y0 + 10))
                self.pantalla.blit(self.fuente.render(
                    f"Costo total g = {paso['g'][self.inicio]}    |    nodos expandidos = {len(paso['Lc'])}",
                    True, C_TEXTO), (10, y0 + 34))
            else:
                self.pantalla.blit(self.fuente_b.render("No existe camino entre SALIDA e INICIO",
                                                        True, C_ROJO), (10, y0 + 10))
        else:
            self.pantalla.blit(self.fuente.render(
                "Avanza con ESPACIO hasta llegar al final para ver el camino completo.",
                True, (90, 90, 90)), (10, y0 + 10))

    def dibujar(self):
        self.pantalla.fill(C_FONDO)
        paso = self.pasos[self.i]
        for n in range(1, self.filas * self.cols + 1):
            self.dibujar_celda(n, paso)
        self.dibujar_camino(paso)
        self.dibujar_flechas(paso)
        self.dibujar_panel(paso)
        self.dibujar_barras(paso)
        pygame.display.flip()

    # ---- entrada ----
    def clic_editar(self, p, teclas):
        n = self.celda_en(p)
        if n is None:
            return
        if teclas[pygame.K_s] and n != self.inicio and n not in self.paredes:
            self.salida = n
        elif teclas[pygame.K_i] and n != self.salida and n not in self.paredes:
            self.inicio = n
        elif n not in (self.salida, self.inicio):
            if n in self.paredes:
                self.paredes.discard(n)
            else:
                self.paredes.add(n)
        self.reiniciar()

    def correr(self):
        corriendo = True
        while corriendo:
            teclas = pygame.key.get_pressed()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    corriendo = False
                elif e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_q, pygame.K_ESCAPE):
                        corriendo = False
                    elif e.key in (pygame.K_SPACE, pygame.K_RIGHT):
                        self.i = min(self.i + 1, len(self.pasos) - 1)
                    elif e.key == pygame.K_LEFT:
                        self.i = max(self.i - 1, 0)
                    elif e.key == pygame.K_f:
                        self.i = len(self.pasos) - 1
                    elif e.key == pygame.K_a:
                        self.auto = not self.auto
                    elif e.key == pygame.K_r:
                        self.i, self.auto = 0, False
                    elif e.key == pygame.K_e:
                        self.editar = not self.editar
                    elif e.key == pygame.K_d:
                        self.cargar(EJEMPLO)
                    elif e.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        self.redimensionar(self.filas + 1, self.cols + 1)
                    elif e.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.redimensionar(self.filas - 1, self.cols - 1)
                    elif e.key == pygame.K_UP:
                        self.redimensionar(self.filas + 1, self.cols)
                    elif e.key == pygame.K_DOWN:
                        self.redimensionar(self.filas - 1, self.cols)
                    elif e.key == pygame.K_PAGEUP:
                        self.redimensionar(self.filas, self.cols + 1)
                    elif e.key == pygame.K_PAGEDOWN:
                        self.redimensionar(self.filas, self.cols - 1)
                    elif e.key == pygame.K_x:
                        self.paredes.clear()
                        self.reiniciar()
                    elif e.key == pygame.K_m:
                        self.aleatorio()
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.editar:
                    self.clic_editar(e.pos, teclas)

            if self.auto and pygame.time.get_ticks() - self.ultimo_auto > 450:
                self.ultimo_auto = pygame.time.get_ticks()
                if self.i < len(self.pasos) - 1:
                    self.i += 1
                else:
                    self.auto = False

            self.dibujar()
            self.reloj.tick(30)
        pygame.quit()


if __name__ == "__main__":
    App().correr()
