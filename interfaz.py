#interfaz grafica del programa
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
        label = tk.Label(self, text=title, font=("Times new roman", 16))
        label.pack()

        if tipo == "Plano":
            self.label3= tk.Label(self, text="Densidad superficial de carga (nC/m)", font=("Times new roman", 14))
            self.label3.pack()
            self.densidad = tk.Entry(self, font=("Times new roman", 14))
            self.densidad.pack()
        elif tipo == "Esfera":
            self.label3 = tk.Label(self, text="Radio de la esfera (m)", font=("Times new roman", 14))
            self.label3.pack()
            self.distancia = tk.Entry(self, font=("Times new roman", 14))
            self.distancia.pack()

            self.label4 = tk.Label(self, text="Carga de la esfera (nC)", font=("Times new roman", 14))
            self.label4.pack()
            self.carga_esfera = tk.Entry(self, font=("Times new roman", 14))
            self.carga_esfera.pack()

        self.label4 = tk.Label(self, text="Datos de la partícula:", font=("Times new roman", 16))
        self.label4.pack()

        self.label5 = tk.Label(self, text="Carga (nC)", font=("Times new roman", 14))
        self.label5.pack()
        self.carga = tk.Entry(self, font=("Times new roman", 14))
        self.carga.pack()

        self.label6 = tk.Label(self, text="Velocidad inicial (m/s)", font=("Times new roman", 14))
        self.label6.pack()
        self.velocidad = tk.Entry(self, font=("Times new roman", 14))
        self.velocidad.pack()

        self.label7 = tk.Label(self, text="Masa (kg)", font=("Times new roman", 14))
        self.label7.pack()
        self.masa = tk.Entry(self, font=("Times new roman", 14))
        self.masa.pack()

        self.calculate_button = tk.Button(self, text="Calcular", command=lambda: self.calcular_distancia(tipo), font=("Times new roman", 14))
        self.calculate_button.pack(pady=10)
        self.result_label = tk.Label(self, text="", font=("Times new roman", 14), fg="green")
        self.result_label.pack(pady=10)

        if tipo == "Esfera":
            self.result_label_v = tk.Label(self, text="", font=("Times new roman", 14), fg="green")
            self.result_label_v.pack(pady=10)
            self.result_label_es = tk.Label(self, text="", font=("Times new roman", 14), fg="green")
            self.result_label_es.pack(pady=10)


    def calcular_distancia(self, tipo):
        masa = float(self.masa.get())
        velocidad = float(self.velocidad.get())
        carga = float(self.carga.get())
        epsilon_0 = 8.854187817e-12  # Valor de la permitividad eléctrica del vacío en F/m
        c = 299792458  # Velocidad de la luz en el vacío (m/s)

        if velocidad > c:
            self.result_label.config(text="Error: La velocidad no puede ser mayor que la velocidad de la luz.")
        else:
            self.result_label.config(text=" ")
            if tipo == "Plano":
                densidad = float(self.densidad.get())
                result = (epsilon_0 * masa * velocidad**2) / (carga * densidad)
                self.result_label.config(text=f"Distancia máxima de alejamiento de la partícula: \n {result} m")
                self.graficar_figura(tipo, result, 0)

            elif tipo == "Esfera":
                distancia = float(self.distancia.get())
                carga_esfera = float(self.carga_esfera.get())
                result_velescape = 0.0
                result_dismax = 0.0
                result_velescape = math.sqrt((masa * carga * carga_esfera) / (math.pi * 2 * epsilon_0 * distancia))
                result_dismax = (2* math.pi* distancia**2 * epsilon_0* velocidad**2) / (carga * carga_esfera)
                self.graficar_figura(tipo, result_dismax, distancia)

                if result_velescape >= c:
                    self.result_label_v.config(text=f"La esfera se ha convertido en un\n AGUJERO NEGRO ELECTROSTÁTICO,\n su velocidad de escape fue \n {result_velescape} m/s \nDistancia máxima de alejamiento de la partícula:\n {result_dismax} m")

                else: 
                    self.result_label_v.config(text=f"Velocidad de escape de la partícula:\n {result_velescape} m/s\nDistancia máxima de alejamiento de la partícula:\n {result_dismax} m")

    
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