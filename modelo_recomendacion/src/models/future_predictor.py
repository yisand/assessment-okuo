# src/models/future_predictor.py
import pandas as pd
from sklearn.pipeline import Pipeline

from src.features.featurize import add_date_features
from src.models.predict import generate_predictions
from src.models.recommend import recommend_top_products


def predict_buyers_for_date(
    model: Pipeline,
    df: pd.DataFrame,
    df_original: pd.DataFrame,
    fecha_objetivo: str,
    prob_threshold: float = 0.5,
) -> pd.DataFrame:
    """
    Predice qué usuarios comprarán en una fecha futura específica y recomienda productos.

    :param model: Modelo entrenado (pipeline sklearn)
    :param df: DataFrame modificado con el resumen de que días realizaron compras los clientes
    :param df_original: Dataframe original con historial de compras
    :param fecha_objetivo: Fecha futura como string "YYYY-MM-DD"
    :param prob_threshold: Umbral mínimo de probabilidad para considerar comprador
    :return: DataFrame con usuario, probabilidad, fecha y productos recomendados
    """
    fecha_objetivo = pd.to_datetime(fecha_objetivo)
    df = df.copy()
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])

    # Última fecha por usuario
    ultimas_fechas = df.groupby("usuario")["fecha_compra"].max().reset_index()
    ultimas_fechas["fecha_objetivo"] = fecha_objetivo
    ultimas_fechas["dias_desde_ultima"] = (fecha_objetivo - ultimas_fechas["fecha_compra"]).dt.days

    # Solo usuarios con alguna diferencia positiva
    candidatos = ultimas_fechas[ultimas_fechas["dias_desde_ultima"] > 0].copy()
    candidatos["fecha_compra"] = candidatos[
        "fecha_objetivo"
    ]  # usar la fecha objetivo como nueva compra

    # Agregar features temporales
    candidatos = add_date_features(candidatos)

    features = ["dias_desde_ultima", "dia_semana", "mes", "dia"]
    print(candidatos)
    X = candidatos[features]
    candidatos["probabilidad"] = generate_predictions(model, X)

    # Filtrar por probabilidad
    compradores = candidatos[candidatos["probabilidad"] >= prob_threshold]
    if compradores.empty:
        return pd.DataFrame(columns=["usuario", "fecha", "probabilidad", "producto"])

    # Recomendar productos
    top_productos = recommend_top_products(df_original)
    resultado = compradores.merge(top_productos, on="usuario", how="left")
    resultado["fecha"] = fecha_objetivo

    return resultado[["usuario", "fecha", "probabilidad", "producto"]]
