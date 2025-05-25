from io import BytesIO
from typing import Any

import boto3
import pandas as pd


def read_csv_from_s3(bucket: str, key: str) -> pd.DataFrame:
    print(f"Leyendo archivo CSV desde S3: s3://{bucket}/{key}")
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj["Body"])
    print(f"Archivo leído. Filas: {len(df)} - Columnas: {list(df.columns)}")
    return df


def filter_recurrent_customers(df: pd.DataFrame) -> pd.DataFrame:
    print("Filtrando compradores recurrentes")
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])

    compras_por_dia = df.groupby(["usuario", "fecha_compra"]).agg(
        {"producto": "count"}
    ).reset_index()
    print(f"Compras por usuario y día: {len(compras_por_dia)} registros")

    compras_grandes = compras_por_dia[compras_por_dia["producto"] > 10]
    print(f"Compras con más de 10 productos: {len(compras_grandes)} registros")

    usuarios_recurrentes = []

    for usuario, compras in compras_grandes.groupby("usuario"):
        fechas = compras["fecha_compra"].sort_values().reset_index(drop=True)
        if len(fechas) < 2:
            continue

        # Calcular diferencias entre compras consecutivas
        diferencias = (fechas - fechas.shift(1)).dropna().dt.days

        # Si todas las diferencias son <= 30 días, es recurrente
        if (diferencias <= 30).all():
            usuarios_recurrentes.append(usuario)

    print(f"Usuarios recurrentes detectados: {len(usuarios_recurrentes)}")

    df_filtrado = df[df["usuario"].isin(usuarios_recurrentes)]
    print(f"Registros filtrados: {len(df_filtrado)}")
    return df_filtrado


def write_parquet_to_s3(df: pd.DataFrame, bucket: str, key: str) -> None:
    print(f"Subiendo archivo a S3: s3://{bucket}/{key}")
    out_buffer = BytesIO()
    df.to_parquet(out_buffer, index=False)
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=out_buffer.getvalue())
    print("Archivo subido correctamente")


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    print("Iniciando ejecución de Lambda")

    bucket = event.get("bucket", "assessment-86fc5eb8")
    key_input = event.get("key_input", "raw-data/data.csv")
    key_output = event.get("key_output", "cleaned-data/AAL286/compradores_recurrentes.parquet")

    df = read_csv_from_s3(bucket, key_input)
    df_filtered = filter_recurrent_customers(df)

    write_parquet_to_s3(df_filtered, bucket, key_output) 

    print("Ejecución finalizada correctamente")

    return {
        "status": "success",
        "rows": len(df_filtered)
    }
