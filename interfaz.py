#interfaz grafica del programa
#Andre Marroquin
#Nelson Garcia
#Problema 5 parcial 2 fisica 3
import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import scatter 
import numpy as np

class PROGRAM(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Partículas Cargadas")
        self.geometry("600x400")

        self.label1 = tk.Label(self, text="Bienvenido al programa de simulación de partículas cargadas.", font=("Times new roman", 16))
        self.label1.pack(pady=10)

        self.label2 = tk.Label(self, text="Por favor, seleccione el tipo de carga central:", font=("Times new roman", 16))
        self.label2.pack()

        self.button_infinite_plane = tk.Button(self, text="Plano Infinito", command=self.open_infinite_plane_screen, font=("Times new roman", 16))
        self.button_infinite_plane.pack(pady=10)

        self.button_sphere = tk.Button(self, text="Esfera", command=self.open_sphere_screen, font=("Times new roman", 16))
        self.button_sphere.pack(pady=10)

    def open_infinite_plane_screen(self):
        self.withdraw()
        InfinitePlaneScreen(self)

    def open_sphere_screen(self):
        self.withdraw()
        SphereScreen(self)
        
    def on_closing(self):        
        self.destroy()
        

class DataEntryFrame(tk.Frame):
    def __init__(self, parent, title, tipo, ax, canvas):
        super().__init__(parent)
        self.pack(side=tk.LEFT, padx=20, pady=20)
        self.ax = ax
        self.canvas = canvas
        label = tk.Label(self, text=title, font=("Times new roman", 14))
        label.pack()

        self.label_par = tk.Label(self, text="Seleccione la partícula:", font=("Times new roman", 13))
        self.label_par.pack()

        self.varpar = tk.StringVar(self)
        self.varpar.trace("w", self.update_var_par)
        self.personalizada_button = ttk.Radiobutton(self, text="Personalizada", variable=self.varpar, value="Personalizada", command=self.update_var_par)
        self.personalizada_button.pack()

        self.protón_button = ttk.Radiobutton(self, text="Protón", variable=self.varpar, value="Protón", command=self.update_var_par)
        self.protón_button.pack()

        self.alfa_button = ttk.Radiobutton(self, text="Alfa", variable=self.varpar, value="Alfa", command=self.update_var_par)
        self.alfa_button.pack()

        self.litio_button = ttk.Radiobutton(self, text="Nucleo de Litio", variable=self.varpar, value="Litio", command=self.update_var_par)
        self.litio_button.pack()

        self.berilio_button = ttk.Radiobutton(self, text="Nucleo de Berilio", variable=self.varpar, value="Berilio", command=self.update_var_par)
        self.berilio_button.pack()

        self.carbono_button = ttk.Radiobutton(self, text="Nucleo de Carbono", variable=self.varpar, value="Carbono", command=self.update_var_par)
        self.carbono_button.pack()

        #self.result_label_par = tk.Label(self, text="", font=("Times new roman", 13), fg="green")
        #self.result_label_par.pack(pady=5)

        if tipo == "Plano":
            self.label3= tk.Label(self, text="Densidad superficial de carga (nC/m)", font=("Times new roman", 12))
            self.label3.pack()
            self.densidad = tk.Entry(self, font=("Times new roman", 12))
            self.densidad.pack()
        elif tipo == "Esfera":
            self.label3 = tk.Label(self, text="Radio de la esfera (m)", font=("Times new roman", 12))
            self.label3.pack()
            self.distancia = tk.Entry(self, font=("Times new roman", 12))
            self.distancia.pack()

            self.label4 = tk.Label(self, text="Carga de la esfera (nC)", font=("Times new roman", 12))
            self.label4.pack()
            self.carga_esfera = tk.Entry(self, font=("Times new roman", 12))
            self.carga_esfera.pack()        

        self.label4 = tk.Label(self, text="Datos de la partícula:", font=("Times new roman", 12))
        self.label4.pack()

        self.label5 = tk.Label(self, text="Carga (nC)", font=("Times new roman", 12))
        self.label5.pack()
        self.carga = tk.Entry(self, font=("Times new roman", 12))
        self.carga.pack()

        self.label6 = tk.Label(self, text="Velocidad inicial (m/s)", font=("Times new roman", 12))
        self.label6.pack()
        self.velocidad = tk.Entry(self, font=("Times new roman", 12))
        self.velocidad.pack()

        self.label7 = tk.Label(self, text="Masa (kg)", font=("Times new roman", 12))
        self.label7.pack()
        self.masa = tk.Entry(self, font=("Times new roman", 12))
        self.masa.pack()

        self.calculate_button = tk.Button(self, text="Calcular", command=lambda: self.calcular_distancia(tipo), font=("Times new roman", 10))
        self.calculate_button.pack(pady=10)        

        self.result_label = tk.Label(self, text="", font=("Times new roman", 12), fg="green")
        self.result_label.pack(pady=10)

    def update_var_par(self, *args):
        # Este método se activará cuando se seleccione una opción en el Combobox
        selected_option = self.varpar.get()
        print(f"Opción seleccionada: {selected_option}")
            

    def calcular_distancia(self, tipo):
        par_tipo = self.varpar.get()
        masa_ = self.masa.get()
        velocidad = self.velocidad.get()
        carga_ = self.carga.get()

        if tipo == "Plano":
            densidad_ = self.densidad.get()
        elif tipo == "Esfera":
            distancia_ = self.distancia.get()
            carga_esfera_ = self.carga_esfera.get()

        epsilon_0 = 8.85e-12  # Valor de la permitividad eléctrica del vacío en F/m
        c = 299792458  # Velocidad de la luz en el vacío (m/s)
        masa = 0.0
        carga = 0.0
        m_p = 1.672621637e-27
        m_n = 1.674927211e-27
        c_p = 1.6021764872e-19

        lista_particulas = ["Personalizada","Protón", "Alfa", "Litio", "Berilio", "Carbono"]
        #carga y masa de las particulas
        lista_valores = [[carga_, masa_], [c_p, m_p],[2*c_p, (2*m_n+2*m_p)] ,[3*c_p,(4*m_n+3*m_p)], [4*c_p,(5*m_n+4*m_p)], [6*c_p,(6*m_n+6*m_p)] ]

        #self.result_label_par.config(text=f"Partícula: {par_tipo}")

        for i in range(len(lista_particulas)):
            if par_tipo == lista_particulas[i]:
                carga = lista_valores[i][0]
                masa = lista_valores[i][1]

        error=0
        
        try:
            # Manejar excepciones si los campos están vacíos o no son números
            if not par_tipo:
                error = error+1
            if par_tipo == "Personalizada":        
                if not masa_:
                    error = error+1
                    if error > 0:
                        raise ValueError("Por favor, ingrese los valores solicitados.")
                    else:
                        raise ValueError("Por favor, ingrese un valor para la masa.")
                if not carga_:
                    error = error+1
                    if error > 0:
                        raise ValueError("Por favor, ingrese un valor para la carga.")
                    else:
                        raise ValueError("Por favor, ingrese un valor para la carga.")
            if not velocidad:
                error = error+1
                if error > 0:
                    raise ValueError("Por favor, ingrese los valores solicitados.")
                else:
                    raise ValueError("Por favor, ingrese un valor para la velocidad.")
            if  tipo == "Plano":
                if not densidad_:
                    error = error+1
                    if error > 0:
                        raise ValueError("Por favor, ingrese un valor para la densidad superficial de carga.")
                    else:
                        raise ValueError("Por favor, ingrese un valor para la densidad superficial de carga.")
            if  tipo == "Esfera":
                if not distancia_:
                    error = error+1
                    if error > 0:
                        raise ValueError("Por favor, ingrese un valor para el radio de la esfera.")
                    else:
                        raise ValueError("Por favor, ingrese un valor para el radio de la esfera.")
                if not carga_esfera_:
                    error = error+1
                    if error > 0:
                        raise ValueError("Por favor, ingrese un valor para la carga de la esfera.")
                    else:
                        raise ValueError("Por favor, ingrese un valor para la carga de la esfera.")
            if error > 0:
                    raise ValueError("Por favor, seleccione una partícula.")
            error=0
            
            masa = float(masa)
            velocidad = float(velocidad)
            carga = float(carga)

            if velocidad > c:
                self.result_label.config(text="Error: La velocidad no puede ser mayor que la velocidad de la luz.")
            else:
                self.result_label.config(text=" ")
                if tipo == "Plano":
                    densidad = float(densidad_)
                    result = (epsilon_0 * masa * velocidad**2) / (carga * densidad)
                    self.result_label.config(text=f"Distancia máxima de alejamiento de la partícula: \n {result} m")
                    self.graficar_figura(tipo, result, 0)

                elif tipo == "Esfera":
                    distancia = float(distancia_)
                    carga_esfera = float(carga_esfera_)
                    result_velescape = 0.0
                    result_dismax = 0.0
                    result_velescape = math.sqrt((carga * carga_esfera) / (math.pi * 2 * epsilon_0 * masa * distancia))
                    result_dismax = (carga * carga_esfera) / (2*math.pi*epsilon_0*masa*velocidad)
                    self.graficar_figura(tipo, result_dismax, distancia)

                    if result_velescape >= c:
                        self.result_label.config(text=f"La esfera se ha convertido en un\n AGUJERO NEGRO ELECTROSTÁTICO,\n su velocidad de escape fue \n {result_velescape} m/s \nDistancia máxima de alejamiento de la partícula:\n {result_dismax} m")

                    else: 
                        self.result_label.config(text=f"Distancia máxima de alejamiento de la partícula:\n {result_dismax} m\nVelocidad de escape de la partícula:\n {result_velescape} m/s")

        except ValueError as e:
            # Manejar excepciones de valores faltantes o no válidos
            error=0
            self.result_label.config(text=str(e))
    
    def graficar_figura(self, tipo, distancia, radio):
        self.ax.clear()
        punto_x = 0
        punto_y = 0

        self.ax.set_xlabel("X (m)")
        self.ax.set_ylabel("Y (m)")
        self.ax.set_title("Distancia máxima de alejamiento de una partícula.")

        if tipo == "Plano":
            self.ax.axhline(y=0, color='blue', linestyle='--', label='Plano Infinito')
            self.ax.legend()
            scatter(punto_x , punto_y + distancia, color='green', marker='o', label='Partícula')
            self.canvas.draw()
        elif tipo == "Esfera":
            phi = np.linspace(0, np.pi, 100)
            theta = np.linspace(0, 2 * np.pi, 100)
            phi, theta = np.meshgrid(phi, theta)
            x = radio * np.sin(phi) * np.cos(theta)
            y = radio * np.sin(phi) * np.sin(theta)
            self.ax.plot(x, y, color='red')
            self.ax.fill(x, y, 'red', alpha=0.2)
            self.ax.axhline(y=radio, color='red', linestyle='--', label='')
            self.ax.legend()
            scatter(punto_x, punto_y + radio + distancia, color='green', marker='o', label='Partícula')
            self.canvas.draw()
        

class InfinitePlaneScreen(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Plano Infinito - Datos de Simulación")
        self.geometry("1100x900")

        self.figure, self.ax = plt.subplots(figsize=(7, 9))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, padx=20, pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        data_entry_frame = DataEntryFrame(self, "Por favor ingrese los datos solicitados a continuación:", "Plano", self.ax, self.canvas)

    def on_closing(self):        
        self.destroy()
        self.parent.deiconify()


class SphereScreen(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Esfera - Datos de Simulación")
        self.geometry("1100x900")

        self.figure, self.ax = plt.subplots(figsize=(7, 9))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, padx=20, pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        data_entry_frame = DataEntryFrame(self, "Por favor ingrese los datos solicitados a continuación:", "Esfera", self.ax, self.canvas)
        
    def on_closing(self):        
        self.destroy()
        self.parent.deiconify()


if __name__ == "__main__":
    correr = PROGRAM()
    correr.mainloop()