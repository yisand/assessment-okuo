import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline


def evaluate_model(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> tuple[str, float]:
    """
    Evalúa el desempeño de un modelo de clasificación utilizando un conjunto de prueba.

    :param model: Modelo entrenado (pipeline de sklearn) que implementa los métodos predict y
      predict_proba.
    :param X_test: Conjunto de características de prueba.
    :param y_test: Valores verdaderos del target para el conjunto de prueba.
    :return: Tupla con el reporte de clasificación (str) y el puntaje AUC (float).
    """
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    return report, auc
