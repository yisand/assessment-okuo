import pandas as pd


def recommend_top_products(df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """
    Recomienda los top-N productos más frecuentes por usuario, basándose en su historial de compras.

    Para cada usuario, se calcula la frecuencia de compra de cada producto y se seleccionan los N
    productos más comprados.

    :param df: DataFrame con columnas 'usuario' y 'producto' representando el historial de compras.
    :param n: Número de productos recomendados por usuario (por defecto 3).
    :return: DataFrame con columnas 'usuario', 'producto' y 'frecuencia', limitado a los top-N por
      usuario.
    """
    return (
        df.groupby(["usuario", "producto"])
        .size()
        .reset_index(name="frecuencia")
        .sort_values(["usuario", "frecuencia"], ascending=[True, False])
        .groupby("usuario")
        .head(n)
    )
