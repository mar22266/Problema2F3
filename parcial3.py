# Función para calcular el valor de η (densidad de partículas)
import math
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

if __name__ == "__main__":
    main()
