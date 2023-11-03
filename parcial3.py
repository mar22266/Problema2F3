# Función para calcular el valor de η (densidad de partículas)
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle

def calcular_densidad_particulas(material):
    #densidades recuperadas de internet
    #duda de las densidades si esta bien o no
    densidades = {
        'oro': 19300,
        'plata': 10490,
        'cobre': 8.49e28,
        'aluminio': 2700,
        'grafito': 2230,
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
    textelectronvel = ax.text(0.05, 0.05, f'Rapidez de Arrastre: {rapidez_arrastre:.2f} m/s', transform=ax.transAxes)

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
        textelectronvel.set_text(f'Rapidez de Arrastre: {rapidez_arrastre:.2f} m/s')
        return electron_lines + [textelectronvel] + alambre_cilindrico + [cilindro_inicio, cilindro_fin]

    ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, repeat=False)
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
    print(f"--------Resumen de resultados:--------")
    print()
    print(f"Valor de η (densidad de partículas) para {material}: {densidad_particulas}")
    print(f"Voltaje aplicado: {voltaje_aplicado}")
    print(f"Resistencia del alambre: {resistencia} ohmios")
    print(f"Corriente: {corriente} amperios")
    print(f"Potencia disipada por el alambre: {potencia} vatios")
    print(f"Rapidez de arrastre de los electrones: {rapidez_arrastre} m/s")
    print(f"Tiempo que le tomará a los electrones atravesar el alambre: {tiempo_atravesar_alambre} segundos")
    mostrar_animacion_electrones_cilindro(largo_alambre, rapidez_arrastre)



if __name__ == "__main__":
    main()
