import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import sympy as sp
import re

# Función para formatear la entrada de la función matemática
def formatear_funcion(func_str):
    func_str = func_str.replace('^', '**')  # Cambio de ^ por **
    func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)  # Multiplicación explícita
    func_str = re.sub(r'(\d)\(', r'\1*(', func_str)  # Multiplicación antes de paréntesis
    return func_str

# Función para calcular el área bajo la curva
def calcular_area(func, a, b):
    try:
        f_lambda = sp.lambdify(x, func, 'numpy')
        area, _ = quad(f_lambda, a, b)
        return area
    except Exception as e:
        print(f"Error al calcular el área: {e}")
        return None

# Función para graficar la curva y calcular el área
def graficar_area(func_str, a, b):
    try:
        func_str = formatear_funcion(func_str)  # Formatear la función
        func = sp.sympify(func_str)  # Convertir el string a una expresión simbólica

        # Validar los límites
        if a > b:
            print("Error: El límite inferior (a) debe ser menor o igual al límite superior (b).")
            return

        f_lambda = sp.lambdify(x, func, 'numpy')  # Función lambda para la evaluación

        # Definir el rango de valores de x para la gráfica
        x_vals = np.linspace(a - 1, b + 1, 1000)  # Aseguramos que cubra todo el rango
        y_vals = f_lambda(x_vals)

        # Crear la figura de la gráfica
        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_vals, label=f'y = {func_str}', color='b', linewidth=2)  # Graficar la curva

        # Rellenar el área bajo la curva entre los límites
        plt.fill_between(x_vals, y_vals, where=(x_vals >= a) & (x_vals <= b), color='skyblue', alpha=0.5, label='Área bajo la curva')

        # Añadir las líneas de los límites
        plt.axvline(a, color='red', linestyle='--', label='Límite Inferior (a)', linewidth=1.5)
        plt.axvline(b, color='green', linestyle='--', label='Límite Superior (b)', linewidth=1.5)

        # Calcular el área bajo la curva
        area = calcular_area(func, a, b)
        if area is None:
            return
        area_formateado = f"{area:.2f}" if area % 1 else f"{int(area)}"

        # Título y texto informativo
        plt.title(f'Área bajo la curva de {func_str}\nÁrea: {area_formateado} m²', fontsize=14, fontweight='bold')
        plt.text((a + b) / 2, max(y_vals) / 2, f'Área: {area_formateado} m²', fontsize=12, ha='center', color='black', style='italic')

        # Ajuste dinámico de límites de la gráfica
        plt.xlim(a - 1, b + 1)
        plt.ylim(min(y_vals) - abs(0.1 * min(y_vals)), max(y_vals) + abs(0.1 * max(y_vals)))

        # Añadir leyenda, cuadrícula y etiquetas
        plt.legend()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)

        # Mostrar la gráfica
        plt.show()

    except sp.SympifyError as e:
        print(f"Error en la función ingresada: {e}")

# Definimos la variable simbólica 'x'
x = sp.symbols('x')

# Entrada del usuario para la función y los límites
func_str = input("Ingrese la función en términos de x (por ejemplo, '5*x^2 + 2*x + 10'): ")
try:
    a = float(input("Ingrese el valor de a (límite inferior): "))
    b = float(input("Ingrese el valor de b (límite superior): "))

    # Llamamos a la función para graficar
    graficar_area(func_str, a, b)
except ValueError:
    print("Error: Por favor ingrese valores numéricos válidos para los límites.")
