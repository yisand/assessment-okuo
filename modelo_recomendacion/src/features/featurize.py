from itertools import product

import pandas as pd


def filter_recurrent_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra los usuarios considerados recurrentes según su comportamiento de compra.

    Un usuario es considerado recurrente si:
    - Ha realizado más de una compra con 10 o más productos.
    - Tiene un promedio de días entre compras menor a 30.

    :param df: DataFrame con el historial de compras, incluyendo columnas 'usuario', 'fecha_compra'
      y 'producto'.
    :return: DataFrame filtrado que contiene únicamente los registros de usuarios recurrentes.
    """
    df = df.copy()
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])

    # Paso 1: identificar usuarios con al menos una compra con 10 o más productos
    grouped = (
        df.groupby(["usuario", "fecha_compra"])
        .agg(cantidad_productos=("producto", "count"))
        .reset_index()
    )
    users_with_big_purchases = grouped[grouped["cantidad_productos"] >= 10]["usuario"].unique()
    df_filtered = df[df["usuario"].isin(users_with_big_purchases)]

    # Paso 2: calcular días entre compras por usuario
    df_sorted = df_filtered.sort_values(by=["usuario", "fecha_compra"])
    df_sorted["days_between_purchases"] = (
        df_sorted.groupby("usuario")["fecha_compra"].diff().dt.days
    )

    # Paso 3: calcular patrones por usuario
    patterns = (
        df_sorted.groupby("usuario")
        .agg(avg_days_between=("days_between_purchases", "mean"))
        .reset_index()
    )

    # Paso 4: seleccionar clientes recurrentes
    MIN_MEAN = 30
    recurrent_users = patterns[(patterns["avg_days_between"] < MIN_MEAN)]["usuario"]

    return df[df["usuario"].isin(recurrent_users)]


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega variables derivadas de la fecha de compra al DataFrame.

    Las variables generadas incluyen:
    - 'dia_semana': Día de la semana (0 = lunes, 6 = domingo).
    - 'mes': Mes numérico de la compra.
    - 'dia': Día del mes.
    - 'dias_desde_ultima': Días transcurridos desde la última compra del usuario.

    :param df: DataFrame que contiene al menos las columnas 'usuario' y 'fecha_compra' en formato
      datetime.
    :return: DataFrame con nuevas columnas de características temporales.
    """
    df = df.copy()
    df["dia_semana"] = df["fecha_compra"].dt.dayofweek
    df["mes"] = df["fecha_compra"].dt.month
    df["dia"] = df["fecha_compra"].dt.day
    df = df.sort_values(by=["usuario", "fecha_compra"])
    df["dias_desde_ultima"] = df.groupby("usuario")["fecha_compra"].diff().dt.days.fillna(0)
    return df


def generate_user_calendar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un calendario diario completo para cada usuario, incluyendo los días sin compras.

    Para cada usuario, se construye una serie de fechas desde la primera hasta la última fecha
    del dataset.
    Luego, se marca con un 1 si el usuario realizó una compra ese día, o 0 en caso contrario.

    Esto permite al modelo aprender también de los días en los que el usuario no compró.

    :param df: DataFrame con columnas 'usuario' y 'fecha_compra', donde cada fila representa
      una compra.
    :return: DataFrame con una fila por usuario y día, incluyendo una columna binaria 'compro'.
    """
    df = df.copy()
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])

    fecha_min = df["fecha_compra"].min()
    fecha_max = df["fecha_compra"].max()
    fechas = pd.date_range(start=fecha_min, end=fecha_max, freq="D")

    usuarios = df["usuario"].unique()
    calendario = pd.DataFrame(product(usuarios, fechas), columns=["usuario", "fecha_compra"])

    df_marcado = df.copy()
    df_marcado["compro"] = 1

    consolidado = calendario.merge(df_marcado, on=["usuario", "fecha_compra"], how="left")
    consolidado["compro"] = consolidado["compro"].fillna(0)
    return consolidado


def group_products_by_customer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las compras por usuario y fecha, calculando totales diarios de cantidad y monto gastado.

    Cada fila del DataFrame resultante representa el resumen de compras de un usuario en un día
    específico.

    :param df: DataFrame original con columnas 'usuario', 'fecha_compra', 'cantidad' y 'precio'.
    :return: DataFrame con columnas 'usuario', 'fecha_compra', 'qty_tot' y 'amount_tot'.
    """
    df = df.groupby(["usuario", "fecha_compra"], as_index=False).agg(
        qty_tot=("cantidad", "sum"),
        amount_tot=("precio", "sum"),
    )
    return df
