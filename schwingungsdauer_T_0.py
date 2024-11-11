import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from uncertainties import ufloat, unumpy
import numpy as np


def find_maxima(x_values, y_values, steps=1):
    # Überprüfen, ob die Länge der Eingabelisten gleich ist
    if len(x_values) != len(y_values):
        raise ValueError

    x_values=x_values[::steps]
    y_values=y_values[::steps]
    maxima = []

    # Durchlaufe den y-Werte-Datensatz, um lokale Maxima zu finden
    for i in range(1, len(y_values) - 1):
        # Ein Hochpunkt liegt vor, wenn der aktuelle y-Wert größer als seine Nachbarn ist
        if y_values[i] >= y_values[i - 1] and y_values[i] >= y_values[i + 1]:
            #if y_values[i] >= y_values[i - 5] and y_values[i] >= y_values[i + 5]:
            maxima.append((x_values[i], y_values[i]))

    return maxima


def plot(df,starting:int=0, steps:int=8, getT=True, T_S=False, messreihe:int=1) -> None:

    zeiten = df[f"Zeit (s) Messreihe #{messreihe}"].str.replace(",", ".").astype(float)
    positionen = df[f"Position (m) Messreihe #{messreihe}"].str.replace(",", ".").astype(float)

    zeiten_nom = unumpy.nominal_values(zeiten)
    positionen_nom = unumpy.nominal_values(positionen)
    zeiten_err = unumpy.std_devs(zeiten)
    positionen_err = unumpy.std_devs(positionen)
    if T_S:
        print(f"=== Schwebedauer: {calc_schwebedauer(zeiten_nom, positionen_nom, [62,92], [1250, 1280])} ===")

    if getT:
        #Berechnung T:
        maxima = find_maxima(zeiten_nom[starting::], positionen_nom[starting::], steps)
        print(maxima)
        print(len(maxima))
        first_max_x = maxima[0][0]
        last_max_x = maxima[len(maxima)-1][0]
        periodendauer = (last_max_x-first_max_x)/(len(maxima)-1)
        print(f"=== Periodendauer: {periodendauer} ===")

    #plot:
    plt.figure(figsize=(15, 5))
    plt.errorbar(zeiten_nom, positionen_nom, fmt=".", label='Messdaten')
    #plt.plot(zeiten_nom, f(zeiten_nom, unumpy.nominal_values(m_fit), unumpy.nominal_values(n_fit)), 'r-',
    #         label=f'Ausgleichsgerade: {m_fit} * x  {n_fit}')
    plt.xlabel('Zeit (s)', fontsize="14")
    plt.ylabel('Position (m)', fontsize="14")
    plt.legend(fontsize="14")
    plt.grid(True)
    plt.show()


def calc_schwebedauer(zeiten, positionen, interwall1:list, interwall2:list) -> float:
    peak1 = find_maxima(zeiten[interwall1[0]:interwall1[1]], positionen[interwall1[0]:interwall1[1]], steps=2)
    peak2 = find_maxima(zeiten[interwall2[0]:interwall2[1]], positionen[interwall2[0]:interwall2[1]], steps=2)
    print(peak1, peak2)
    return peak2[0][0] - peak1[0][0]


if __name__ == "__main__":
    #df1 = pd.read_csv("daten/Daten1.csv", delimiter=";")
    #plot(df1, 404,6)
    #df2 = pd.read_csv("daten/Daten2.csv", delimiter=";")
    #plot(df2, 100,3)
    df3 = pd.read_csv("daten/DatenKupferTS.csv", delimiter=";")
    plot(df3, getT=False, T_S=True)
    # TODO: auf minima wechseln
    #df4 = pd.read_csv("daten/DatenKupferTGL.csv", delimiter=";")
    #plot(df4, messreihe=2, starting=30, steps=1)
    #df5 = pd.read_csv("daten/DatenKupferTGEG.csv", delimiter=";")
    #plot(df5, messreihe=5, starting=30, steps=2)


    # TODO: Parameter anpassen
    df3 = pd.read_csv("daten/DatenStahlTS.csv", delimiter=";")
    plot(df3, messreihe=6, getT=False, T_S=False)
    df4 = pd.read_csv("daten/DatenStahlTGL.csv", delimiter=";")
    plot(df4, starting=30, steps=5)
    df5 = pd.read_csv("daten/DatenStahlTGEG.csv", delimiter=";")
    plot(df5, messreihe=5, starting=30, steps=5)

