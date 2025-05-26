import boto3
import pandas as pd


def load_batch_data(bucket: str, key: str) -> pd.DataFrame:
    """
    Carga un archivo CSV desde un bucket de S3 y lo retorna como un DataFrame de pandas.

    :param bucket: Nombre del bucket de S3 donde se encuentra el archivo.
    :param key: Ruta (clave) del archivo dentro del bucket.
    :return: DataFrame con el contenido del archivo CSV cargado desde S3.
    """
    print(f"Leyendo archivo CSV desde S3: s3://{bucket}/{key}")
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(obj["Body"])
    print(f"Archivo leído. Filas: {len(df)} - Columnas: {list(df.columns)}")
    return df
