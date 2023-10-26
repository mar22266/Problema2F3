#Problema  parcial 2
#Andre Marroquin 
#Nelson Garcia
import math

# Constante de permitividad del vacío
epsilon_0 = 8.854187817e-12  # (F/m)

def main():
    print("Simulación de partícula cargada interactuando con una superficie cargada")
    
    # Solicitar al usuario el tipo de carga central (esfera o plano)
    tipo_carga = input("Tipo de carga (esfera/plano): ").lower()
    
    if tipo_carga == "esfera":
        radio = float(input("Radio de la esfera (metros): "))
        carga_esfera = float(input("Carga de la esfera (Coulombs): "))
        masa_particula = float(input("Masa de la partícula (kilogramos): "))
        velocidad_inicial = float(input("Velocidad inicial de la partícula (m/s): "))
        
        distancia_maxima, velocidad_escape = calcular_distancia_maxima_esfera(radio, carga_esfera, masa_particula, velocidad_inicial)
        
    elif tipo_carga == "plano":
        densidad_superficial = float(input("Densidad superficial de carga (Coulombs/m^2): "))
        masa_particula = float(input("Masa de la partícula (kilogramos): "))
        velocidad_inicial = float(input("Velocidad inicial de la partícula (m/s): "))
        
        distancia_maxima = calcular_distancia_maxima_plano(densidad_superficial, masa_particula, velocidad_inicial)
        velocidad_escape = None  # No aplicable al plano
    
    else:
        print("Tipo de carga no válido. Debe ser 'esfera' o 'plano'.")
        return

    # Comprobar si la esfera se ha convertido en un agujero negro electrostático
    if distancia_maxima < 0:
        print("La esfera se ha convertido en un agujero negro electrostático.")
    else:
        print(f"Distancia máxima de alejamiento: {distancia_maxima} metros")
    
    if velocidad_escape is not None:
        print(f"Velocidad de escape: {velocidad_escape} m/s")

def calcular_distancia_maxima_esfera(radio, carga_esfera, masa_particula, velocidad_inicial):
    # Cálculo de la velocidad de escape
    velocidad_escape = math.sqrt(2 * carga_esfera / (4 * math.pi * epsilon_0 * radio * masa_particula))
    
    # Comprobar si la velocidad inicial excede la velocidad de la luz en el vacío
    if velocidad_inicial > 299792458:
        return -1, velocidad_escape  # La partícula no puede superar la velocidad de la luz
    
    # Cálculo de la distancia máxima de alejamiento
    distancia_maxima = (masa_particula * velocidad_inicial ** 2) / (2 * carga_esfera / (4 * math.pi * epsilon_0 * radio))
    
    return distancia_maxima, velocidad_escape

def calcular_distancia_maxima_plano(densidad_superficial, masa_particula, velocidad_inicial):
    # Cálculo de la distancia máxima de alejamiento en el caso del plano
    distancia_maxima = (masa_particula * velocidad_inicial ** 2) / (2 * densidad_superficial)
    
    return distancia_maxima

if __name__ == "__main__":
    main()
