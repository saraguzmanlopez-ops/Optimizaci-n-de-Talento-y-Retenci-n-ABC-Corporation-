
# Importación de librerías

import pandas as pd


"""
Funciones de soporte para la gestión de valores nulos.

Encontramos funciones reutilizables para aplicar imputaciones de forma homogénea durante la fase de transformación de datos.
"""


def imputar_moda(df, lista_columnas, verbose=True):
    """
    Imputa los valores nulos de las columnas indicadas utilizando la moda de cada variable.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame sobre el que se realizará la imputación.
    lista_columnas : list
        Lista con los nombres de las columnas a imputar.
    verbose : bool, optional
        Si es True, muestra por pantalla el valor usado en cada imputación.

    Devuelve
    -------
    pandas.DataFrame
        DataFrame con los valores nulos imputados.
    """
    for col in lista_columnas:
        if df[col].mode().empty:
            continue

        moda = df[col].mode()[0]
        df[col] = df[col].fillna(moda)

        if verbose:
            print(f"Columna '{col}': valores nulos reemplazados por la moda -> '{moda}'")

    return df


def imputar_mediana(df, dicc_columnas, verbose=True):
    """
    Imputa los valores nulos de una o varias columnas utilizando la mediana calculada dentro de un grupo de referencia.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame sobre el que se realizará la imputación.
    dicc_columnas : dict
        Diccionario donde la clave es la columna a imputar y el valor es la columna utilizada para agrupar.
    verbose : bool, optional
        Si es True, muestra el criterio aplicado.

    Devuelve
    -------
    pandas.DataFrame
        DataFrame con los valores nulos imputados.
    """
    for col_objetivo, col_grupo in dicc_columnas.items():
        mediana = df.groupby(col_grupo)[col_objetivo].transform("median")
        df[col_objetivo] = df[col_objetivo].fillna(mediana)

        if verbose:
            print(f"Columna '{col_objetivo}': valores nulos imputados por la mediana de '{col_grupo}'")

    return df