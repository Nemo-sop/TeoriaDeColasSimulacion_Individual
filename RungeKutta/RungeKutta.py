from random import random
import pandas as pd


def calcularRK():
    " Ecuación diferencial: DA/dt = B * A"
    # valorBeta = distribuciones.uniforme(0, 1)
    ecDif = lambda t, X: 0.5 * X*X - (0.2*X) + 5
    valor, dfRungeKutta = rungeKutta(ecDif, 0, 0)
    return valor, dfRungeKutta


def rungeKutta(fun, xi, yi):
    dfRungeKutta = pd.DataFrame(
        {"xi": [], "yi": [], "k1": [], "k2": [], "k3": [], "k4": [], "xi+1": [], "yi+1": []})
    h = 0.001
    while yi < 180:
        fila = pd.DataFrame({"xi": [], "yi": [], "k1": [], "k2": [], "k3": [], "k4": [], "xi+1": [], "yi+1": []})

        k1 = fun(xi, yi)
        k2 = fun(xi + h / 2, yi + h / 2 * k1)
        k3 = fun(xi + h / 2, yi + h / 2 * k2)
        k4 = fun(xi + h, yi + h * k3)

        fila.at[0, "xi"] = xi
        fila.at[0, "yi"] = yi

        yi = yi + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        xi += h

        fila.at[0, "k1"] = k1
        fila.at[0, "k2"] = k2
        fila.at[0, "k3"] = k3
        fila.at[0, "k4"] = k4
        fila.at[0, "xi+1"] = xi
        fila.at[0, "yi+1"] = yi

        dfRungeKutta = pd.concat([dfRungeKutta, fila], ignore_index=True)

    return round(xi*60, 4), dfRungeKutta

# pd.set_option('display.max_rows', None)
# x, df = calcularRK()
#
# print(df)
# print(x)