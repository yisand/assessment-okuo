import joblib
from dotenv import load_dotenv
from src.data.load_data import load_batch_data
from src.evaluation.metrics import evaluate_model
from src.features.featurize import (
    add_date_features,
    filter_recurrent_customers,
    generate_user_calendar,
    group_products_by_customer,
)
from src.models.train import train_model_chronological
from src.utils.utils import print_banner

load_dotenv()


def main() -> None:
    bucket = "assessment-86fc5eb8"
    key_input = "raw-data/data.csv"
    model_output_path = "output/model.pkl"

    print_banner("Cargando datos")
    df = load_batch_data(bucket, key_input)
    df = filter_recurrent_customers(df)
    df = group_products_by_customer(df)
    df = generate_user_calendar(df)
    df = add_date_features(df)

    features = ["dias_desde_ultima", "dia_semana", "mes", "dia"]
    model, X_test, y_test = train_model_chronological(df, features=features, target="compro")
    report, auc = evaluate_model(model, X_test, y_test)

    print_banner("Evaluación")
    print(report)
    print(f"AUC: {auc:.4f}")

    print_banner("Guardando modelo")
    joblib.dump(model, model_output_path)
    print(f"Modelo guardado en {model_output_path}")


if __name__ == "__main__":
    main()
