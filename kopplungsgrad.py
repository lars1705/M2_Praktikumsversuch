import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from uncertainties import ufloat, unumpy
import numpy as np

#constants
X_20_BRAUN = 66
X_10_BRAUN = 32.5
X_20_GRAU = 61.6
X_10_GRAU = 36

DELTA_X = 0.1/np.sqrt(6)

def f(x, m, n):
    return m*x+n


def plot_geraden_anpassung(x_1s:list, x_2s:list) -> None:
    #steigung = x_2 / x_1 = k
    #dabei wird x_1 manuell ausgelenkt

    x1_nom = unumpy.nominal_values(x_1s)
    x2_nom = unumpy.nominal_values(x_2s)
    x1_err = unumpy.std_devs(x_1s)
    x2_err = unumpy.std_devs(x_2s)

    params, params_covariance = curve_fit(f, x1_nom, x2_nom, p0=[1,0], sigma=x2_err, absolute_sigma=True)
    m_fit, n_fit = ufloat(params[0], np.sqrt(params_covariance[0,0])), ufloat(params[1], np.sqrt(params_covariance[1,1]))

    print(f"=== k={m_fit} ===")


    plt.figure(figsize=(10, 6))
    plt.errorbar(x1_nom, x2_nom, xerr=DELTA_X, yerr=DELTA_X, fmt=".", label='Messdaten')
    plt.plot(x1_nom, f(x1_nom, unumpy.nominal_values(m_fit), unumpy.nominal_values(n_fit)), 'r-',
             label=f'Ausgleichsgerade: {m_fit} * x  {n_fit}')
    plt.xlabel(r'$x_1$', fontsize="14")
    plt.ylabel(r'$x_2$', fontsize="14")
    plt.legend(fontsize="14")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv("daten/daten_kopplungsgrad.csv", delimiter=";")
    x_1sb = [ufloat(X_10_BRAUN - x, DELTA_X) for x in df["x_1 braune Feder"].values]
    x_2sb = [ufloat(X_20_BRAUN - x, DELTA_X) for x in df["x_2 braune Feder"].values]

    x_1sg = [ufloat(X_10_GRAU - x, DELTA_X) for x in df["x_1 graue Feder"].values]
    x_2sg = [ufloat(X_20_GRAU - x, DELTA_X) for x in df["x_2 graue Feder"].values]

    plot_geraden_anpassung(x_1sb, x_2sb)
    plot_geraden_anpassung(x_1sg, x_2sg)
