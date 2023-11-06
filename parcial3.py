# Función para calcular el valor de η (densidad de partículas)
#Problema 5 Parcial 3
#Andre marroquin
#Nelson Garcia
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
import random
from colorama import Fore, Back, Style, init

# Inicializa colorama para que funcione en sistemas Windows
init()

def calcular_densidad_particulas(material):
    #densidades recuperadas de internet
    #duda de las densidades si esta bien o no
    densidades = {
        'oro': 5.9e28,
        'plata': 5.8e28,
        'cobre': 8.5e28,
        'aluminio': 6.0245e31,
        'grafito': 3.2421e30,
    }
    if material in densidades:
        return densidades[material]
    else:
        return None

def obtener_resistividad(material):
    # resistividades recuperadas del libro de fsica utilizado en el curso ( a temperatura ambiente 20°C)
    resistividades = {
        'oro': 2.44e-8,    # Ohmios por metro
        'plata': 1.47e-8,  # Ohmios por metro
        'cobre': 1.72e-8,  # Ohmios por metro
        'aluminio': 2.75e-8,  # Ohmios por metro
        'grafito': 3.5e-5,  # Ohmios por metro
    }
    if material in resistividades:
        return resistividades[material]
    else:
        return None


def verificar_numero(cadena):
    try:
        float(cadena)  # Intenta convertir la cadena a un número decimal
        if "." in cadena:
            return "decimal"
        else:
            return "entero"
    except ValueError:
        return "no es un número"

# Función para calcular el diámetro en mm a partir del calibre AWG
def awg_a_mm(awg):
    return 0.127 * 92 ** ((36 - awg) / 39)

# Función para calcular el calibre AWG a partir del diámetro en mm
def mm_a_awg(mm):
    return 36 - 39 * math.log(mm / 0.127) / math.log(92)

# Función para calcular la resistencia del alambre
def calcular_resistencia(largo, diametro, material):
    resistividad = obtener_resistividad(material)
    if resistividad is not None:
        area = math.pi * (diametro / 2000) ** 2
        resistencia = resistividad * (largo / area)
        return resistencia
    else:
        return None


# Función para calcular la corriente
def calcular_corriente(voltaje, resistencia):
    corriente = voltaje / resistencia
    return corriente

# Función para calcular la potencia disipada por el alambre
def calcular_potencia(voltaje, corriente):
    potencia = voltaje * corriente
    return potencia

# Función para calcular la rapidez de arrastre de los electrones
def calcular_rapidez_arrastre(corriente, densidad_particulas,diametro):
    carga_elemental = 1.6e-19  # Carga elemental en Coulombs
    area = math.pi * (diametro / 2000) ** 2
    rapidez = corriente / (densidad_particulas * carga_elemental *area)
    return rapidez

# Función para calcular el tiempo que le tomará a los electrones atravesar el alambre
def calcular_tiempo(largo, rapidez):
    tiempo = largo / rapidez
    return tiempo




# Función para mostrar una animación de los electrones y un cilindro a lo largo del alambre
def mostrar_animacion_electrones_cilindro(largo_alambre, rapidez_arrastre):
    tiempo_total = largo_alambre / rapidez_arrastre  # Duración de la animación en segundos
    num_electrones = 10  # Número de electrones para la animación
    num_frames = 100  # Número de fotogramas para la animación

    tiempo = np.linspace(0, tiempo_total, num_frames)
    posiciones_electron = tiempo * rapidez_arrastre
    posiciones_electron = posiciones_electron % largo_alambre  # Asegurar que los electrones no salgan del alambre

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, largo_alambre)
    ax.set_ylim(-0.1, 0.1)
    ax.set_xlabel("Posición en el alambre (metros)")
    ax.set_title("Simulación de Movimiento de Electrones")
    ax.grid(True)

    electron_lines = []
    textelectronvel = ax.text(0.05, 0.05, f'Rapidez de Arrastre: {rapidez_arrastre:.16f} m/s', transform=ax.transAxes)

    for i in range(num_electrones):
        electron_line, = ax.plot([], [], 'bo', markersize=10)
        electron_lines.append(electron_line)

    # Agregar un cilindro a lo largo del alambre
    alambre_cilindrico = []
    cilindro_radio = 0.05  # Radio del cilindro
    cilindro_altura = 0.1  # Altura del cilindro

    for x in np.arange(0, largo_alambre, cilindro_radio * 2):
        cilindro = Rectangle((x, -cilindro_altura / 2), cilindro_radio * 2, cilindro_altura, fill=True, color='gray')
        ax.add_patch(cilindro)
        alambre_cilindrico.append(cilindro)

    # Agregar círculos en los extremos del cilindro (negros)
    cilindro_inicio = Circle((0, 0), cilindro_radio, fill=True, color='black')
    ax.add_patch(cilindro_inicio)
    cilindro_fin = Circle((largo_alambre, 0), cilindro_radio, fill=True, color='black')
    ax.add_patch(cilindro_fin)

    def init():
        for line in electron_lines:
            line.set_data([], [])
        return electron_lines + [textelectronvel] + alambre_cilindrico + [cilindro_inicio, cilindro_fin]

    def update(frame):
        for i in range(num_electrones):
            electron_lines[i].set_data(posiciones_electron[frame] + i * 0.1, 0)
        textelectronvel.set_text(f'Rapidez de Arrastre: {rapidez_arrastre:.16f} m/s')
        return electron_lines + [textelectronvel] + alambre_cilindrico + [cilindro_inicio, cilindro_fin]

    ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, repeat=False)
    plt.show()


def mostrar_animacion_electrones_aleatorios(largo_alambre, num_electrones, num_circulos):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, largo_alambre)
    ax.set_ylim(-0.1, 0.1)
    ax.set_xlabel("Posición en el alambre (metros)")
    ax.set_title("Simulación de Movimiento de Electrones Aleatorios")
    ax.grid(True)

    # Crear el cilindro
    # Agregar un cilindro a lo largo del alambre
    alambre_cilindrico = []
    cilindro_radio = 0.05  # Radio del cilindro
    cilindro_altura = 0.1  # Altura del cilindro

    for x in np.arange(0, largo_alambre, cilindro_radio * 2):
        cilindro = Rectangle((x, -cilindro_altura / 2), cilindro_radio * 2, cilindro_altura, fill=True, color='gray')
        ax.add_patch(cilindro)
        alambre_cilindrico.append(cilindro)

    # Agregar círculos en los extremos del cilindro (negros)
    cilindro_inicio = Circle((0, 0), cilindro_radio, fill=True, color='black')
    ax.add_patch(cilindro_inicio)
    cilindro_fin = Circle((largo_alambre, 0), cilindro_radio, fill=True, color='black')
    ax.add_patch(cilindro_fin)

    etiqueta = ax.text(0.02, 0.92, 'Círculos azules: Electrones\nCírculos rojos: Átomos', transform=ax.transAxes, fontsize=10,
                       bbox={'facecolor': 'white', 'edgecolor': 'gray', 'alpha': 0.7})

    # Crear los círculos rojos alrededor del cilindro
    circulos = []
    circulo_radio = 0.01
    for i in range(num_circulos):
        x = random.uniform(0, largo_alambre)
        y = random.uniform(-0.05, 0.05)
        circulo = Circle((x, y), circulo_radio, fill=True, color='red')
        ax.add_patch(circulo)
        circulos.append(circulo)

    # Crear los electrones
    electrones = []
    for i in range(num_electrones):
        x = random.uniform(0, largo_alambre)
        y = random.uniform(-0.05, 0.05)
        electron = plt.scatter(x, y, color='blue', s=50)
        electrones.append(electron)

    def init():
        return circulos + electrones

    def update(frame):
        for electron in electrones:
            # Mueve el electrón a un círculo aleatorio
            circulo_destino = random.choice(circulos)
            x, y = circulo_destino.center
            electron.set_offsets([x, y])

    ani = animation.FuncAnimation(fig, update, init_func=init, frames=100, interval=200, repeat=False)
    plt.show()

# Función principal
def main():
    largo_alambre = float(input("Ingrese el largo del alambre en metros: "))
    calibre = input("Ingresa un valor (calibre AWG o diámetro en mm) si es en AWG ingrese un entero si es en mm ingrese el valor con decimal: ")
    
    tipo = verificar_numero(calibre)
    
    if tipo == "decimal":
        diametro_mm = float(calibre)
        calibre_awg = mm_a_awg(diametro_mm)
        print()
        print(f"El diámetro en mm es: {diametro_mm}")
        print(f"El calibre AWG equivalente es: {calibre_awg}")
        print()
    elif tipo == "entero":
        calibre_awg = int(calibre)
        diametro_mm = awg_a_mm(calibre_awg)
        print()
        print(f"El calibre AWG es: {calibre_awg}")
        print(f"El diámetro en mm equivalente es: {diametro_mm}")
        print()
    else:
        print("El valor ingresado no es válido.")

    material = input("Ingrese el material del conductor (oro, plata, cobre, aluminio o grafito): ")
    densidad_particulas = calcular_densidad_particulas(material)
    if densidad_particulas is None:
        print("El material ingresado no es válido.")
        return

    voltaje_aplicado = float(input("Ingrese el voltaje aplicado en voltios: "))

    resistencia = calcular_resistencia(largo_alambre, diametro_mm, material)
    corriente = calcular_corriente(voltaje_aplicado, resistencia)
    potencia = calcular_potencia(voltaje_aplicado, corriente)
    rapidez_arrastre = calcular_rapidez_arrastre(corriente, densidad_particulas,diametro_mm)
    tiempo_atravesar_alambre = calcular_tiempo(largo_alambre, rapidez_arrastre)

    print()
    print(Fore.BLUE, end="")
    print(f"--------Resumen de resultados:--------")
    print()
    print(Style.RESET_ALL, end="")

    # Establece el color verde para todo el bloque de texto
    print(f"Valor de η (densidad de partículas) para {material}: {Fore.GREEN}{densidad_particulas}{Fore.RESET}")
    print(f"Voltaje aplicado: {Fore.GREEN}{voltaje_aplicado} volts{Fore.RESET}")
    print(f"Resistencia del alambre: {Fore.GREEN}{resistencia} ohmios{Fore.RESET} ")
    print(f"Corriente: {Fore.GREEN}{corriente} amperios{Fore.RESET} ")
    print(f"Potencia disipada por el alambre:  {Fore.GREEN}{potencia} vatios{Fore.RESET} ")
    print(f"Rapidez de arrastre de los electrones:  {Fore.GREEN}{rapidez_arrastre} m/s{Fore.RESET}")
    print(f"Tiempo que le tomará a los electrones atravesar el alambre:  {Fore.GREEN}{tiempo_atravesar_alambre} segundos{Fore.RESET}")
    print(Style.RESET_ALL, end="")
    print(Fore.BLUE, end="")
    print()
    print("---------------------------------------")
    print(Style.RESET_ALL, end="")
    print()
    print()
    
    mostrar_animacion_electrones_aleatorios(largo_alambre=0.5, num_electrones=1, num_circulos=10)
    mostrar_animacion_electrones_cilindro(largo_alambre, rapidez_arrastre)



if __name__ == "__main__":
    main()
