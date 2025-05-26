import joblib
from dotenv import load_dotenv
from src.data.load_data import load_batch_data
from src.features.featurize import (
    add_date_features,
    filter_recurrent_customers,
    generate_user_calendar,
    group_products_by_customer,
)
from src.models.future_predictor import predict_buyers_for_date
from src.utils.utils import print_banner

load_dotenv()


def main() -> None:
    bucket = "assessment-86fc5eb8"
    key_input = "raw-data/data.csv"
    fecha_prediccion = "2014-12-29"
    output_file = "reports/prediccion_futura.csv"
    model_input_path = "output/model.pkl"

    print_banner("Cargando datos")
    df = load_batch_data(bucket, key_input)
    df = filter_recurrent_customers(df)
    df_original = df.copy()
    df = group_products_by_customer(df)
    df = generate_user_calendar(df)
    df = add_date_features(df)

    print_banner("Cargando modelo")
    model = joblib.load(model_input_path)

    print_banner(f"Prediciendo compradores para {fecha_prediccion}")
    resultados = predict_buyers_for_date(
        model, df, df_original, fecha_objetivo=fecha_prediccion, prob_threshold=0.5
    )
    resultados.to_csv(output_file, index=False)

    print_banner("Resultados guardados")
    print(resultados.head())


if __name__ == "__main__":
    main()
