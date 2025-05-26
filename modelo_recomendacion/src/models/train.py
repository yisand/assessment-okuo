import pandas as pd
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier


def train_model_chronological(
    df: pd.DataFrame, features: list[str], target: str
) -> tuple[Pipeline, pd.DataFrame, pd.Series]:
    """
    Entrena un modelo de clasificación utilizando una división cronológica del dataset.

    El DataFrame se ordena por fecha y se divide en un 80% inicial para entrenamiento y 20% final
    para prueba.
    Se utiliza un pipeline con estandarización y un clasificador XGBoost, ajustando el parámetro
    'scale_pos_weight' para manejar desbalanceo en la variable objetivo.

    :param df: DataFrame con las variables de entrada, incluyendo una columna de fecha llamada
      'fecha_compra'.
    :param features: Lista de nombres de columnas que serán utilizadas como características del
      modelo.
    :param target: Nombre de la columna objetivo a predecir.
    :return: Tupla que contiene el modelo entrenado, el conjunto de prueba X_test y las etiquetas
      reales y_test.
    """
    df = df.sort_values("fecha_compra")
    corte = int(len(df) * 0.8)
    train_df = df.iloc[:corte]
    test_df = df.iloc[corte:]

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

    model = make_pipeline(
        StandardScaler(with_mean=False),
        XGBClassifier(
            learning_rate=0.1,
            max_depth=5,
            scale_pos_weight=y_train.value_counts()[0] / y_train.value_counts()[1],
            n_jobs=-1,
        ),
    )
    model.fit(X_train, y_train)
    return model, X_test, y_test
