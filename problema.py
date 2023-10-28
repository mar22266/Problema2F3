#Problema  parcial 2
#Andre Marroquin 
#Nelson Garcia
import pygame
import sys
import math

# Inicialización de Pygame
pygame.init()

# Constantes físicas
k = 8.99e9  # Constante de Coulomb
c = 299792458  # Velocidad de la luz en el vacío (m/s)

# Configuración de la ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulación de Partícula y Carga")

# Clase para representar la partícula
class Particula:
    def __init__(self, x, y, carga, velocidad):
        self.x = x
        self.y = y
        self.carga = carga
        self.velocidad = velocidad

    def mover(self):
        # Implementa el movimiento de la partícula según las fuerzas electrostáticas
        pass

    def dibujar(self):
        # Dibuja la partícula en la pantalla
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 10)

# Clase para representar la carga (plano o esfera)
class Carga:
    def __init__(self, x, y, carga):
        self.x = x
        self.y = y
        self.carga = carga

    def fuerza_electrica(self, particula):
        # Calcula la fuerza eléctrica entre la carga y la partícula
        dx = particula.x - self.x
        dy = particula.y - self.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)
        fuerza = (k * particula.carga * self.carga) / distancia ** 2
        angulo = math.atan2(dy, dx)
        fx = fuerza * math.cos(angulo)
        fy = fuerza * math.sin(angulo)
        return fx, fy

    def dibujar(self):
        # Dibuja la carga en la pantalla
        pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), 20)

# Función para calcular la distancia de máximo alejamiento
def distancia_maxima(particula, carga):
    distancia_maxima = 0
    while True:
        fx, fy = carga.fuerza_electrica(particula)
        particula.x += particula.velocidad
        particula.y -= fy
        distancia = math.sqrt((particula.x - carga.x) ** 2 + (particula.y - carga.y) ** 2)
        if distancia > distancia_maxima:
            distancia_maxima = distancia
        if distancia < 20:
            return distancia_maxima

# Entrada de parámetros
tipo_carga = input("Tipo de carga (esfera o plano): ")
radio = 0
carga = 0
densidad_superficial = 0

if tipo_carga == "esfera":
    radio = float(input("Radio de la esfera (m): "))
    carga = float(input("Carga distribuida homogéneamente en la esfera (Coulombs): "))
elif tipo_carga == "plano":
    densidad_superficial = float(input("Densidad superficial de carga en el plano (C/m^2): "))

carga_particula = float(input("Carga de la partícula (Coulombs): "))
masa_particula = float(input("Masa de la partícula (kg): "))
rapidez_inicial = float(input("Rapidez inicial de la partícula (m/s): "))

# Inicialización de la partícula y la carga
particula = Particula(100, 100, carga_particula, rapidez_inicial)
carga = Carga(400, 300, carga)

# Cálculo de la distancia de máximo alejamiento
distancia_max = distancia_maxima(particula, carga)
print("Distancia de máximo alejamiento: {:.2f} metros".format(distancia_max))

# Verificación de velocidad de escape
velocidad_escape = math.sqrt((2 * k * abs(carga.carga)) / carga_particula)
if rapidez_inicial >= velocidad_escape:
    print("La partícula ha alcanzado la velocidad de escape.")
else:
    print("La partícula no ha alcanzado la velocidad de escape.")
    if carga.carga < 0 and carga_particula > velocidad_escape:
        print("La esfera se ha convertido en un agujero negro electrostático.")

# Bucle principal
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calcula la fuerza eléctrica y mueve la partícula
    fx, fy = carga.fuerza_electrica(particula)
    particula.x += particula.velocidad
    particula.y -= fy

    # Limpia la pantalla
    screen.fill((255, 255, 255))

    # Dibuja la carga y la partícula
    carga.dibujar()
    particula.dibujar()

    pygame.display.update()
    clock.tick(60)
