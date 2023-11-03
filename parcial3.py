# Función para calcular el valor de η (densidad de partículas)
def calcular_densidad_particulas(material):
    densidades = {
        'oro': 19.32,
        'plata': 10.49,
        'cobre': 8.96,
        'aluminio': 2.70,
        'grafito': 2.26,
    }
    if material in densidades:
        return densidades[material]
    else:
        return None

def obtener_resistividad(material):
    resistividades = {
        'oro': 2.44e-8,    # Ohmios por metro
        'plata': 1.59e-8,  # Ohmios por metro
        'cobre': 1.68e-8,  # Ohmios por metro
        'aluminio': 2.82e-8,  # Ohmios por metro
        'grafito': 1.00e-5,  # Ohmios por metro
    }
    if material in resistividades:
        return resistividades[material]
    else:
        return None

# Función para calcular el diámetro en mm a partir del calibre AWG
def awg_a_mm(awg):
    return 0.127 * 92 ** ((36 - awg) / 39)

# Función para calcular la resistencia del alambre
def calcular_resistencia(largo, diametro, material):
    resistividad = obtener_resistividad(material)
    if resistividad is not None:
        area = 3.14159 * (diametro / 2000) ** 2
        resistencia = resistividad * (largo / area)
        print(f"Resistencia calculada: {resistencia} ohmios")
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
    carga_elemental = 1.60219e-19  # Carga elemental en Coulombs
    area = 3.14159 * (diametro / 2000) ** 2
    rapidez = corriente / (densidad_particulas * carga_elemental *area)
    return rapidez

# Función para calcular el tiempo que le tomará a los electrones atravesar el alambre
def calcular_tiempo(largo, rapidez):
    tiempo = largo / rapidez
    return tiempo

# Función principal
def main():
    largo_alambre = float(input("Ingrese el largo del alambre en metros: "))
    calibre = input("Ingrese el calibre (mm o AWG): ")
    if calibre.isnumeric():
        diametro_mm = float(calibre)
    elif calibre.isdigit():
        diametro_mm = awg_a_mm(int(calibre))
    else:
        print("El calibre ingresado no es válido.")
        return

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

    print(f"Valor de η (densidad de partículas) para {material}: {densidad_particulas}")
    print(f"Voltaje aplicado: {voltaje_aplicado}")
    print(f"Resistencia del alambre: {resistencia} ohmios")
    print(f"Corriente: {corriente} amperios")
    print(f"Potencia disipada por el alambre: {potencia} vatios")
    print(f"Rapidez de arrastre de los electrones: {rapidez_arrastre} m/s")
    print(f"Tiempo que le tomará a los electrones atravesar el alambre: {tiempo_atravesar_alambre} segundos")

if __name__ == "__main__":
    main()
