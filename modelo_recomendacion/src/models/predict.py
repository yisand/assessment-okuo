import pandas as pd
from sklearn.pipeline import Pipeline


def generate_predictions(model: Pipeline, X: pd.DataFrame) -> pd.Series:
    """
    Genera las probabilidades de que ocurra una compra futura utilizando un modelo entrenado.

    Devuelve la probabilidad de la clase positiva (compra = 1) para cada muestra del conjunto de
    entrada.

    :param model: Modelo de clasificación entrenado (pipeline de sklearn) con soporte para
      predict_proba.
    :param X: DataFrame con las características de entrada para generar predicciones.
    :return: Serie de pandas con las probabilidades de compra, indexada igual que X.
    """
    return pd.Series(model.predict_proba(X)[:, 1], index=X.index)
