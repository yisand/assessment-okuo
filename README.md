
# Recomendador de Compras + ETL Lambda

Este repositorio contiene dos componentes principales desarrollados para la prueba técnica de datos de Okuo:

1. **ETL en AWS Lambda (Dockerizada)** que transforma los datos crudos desde S3.
2. **Modelo de Recomendación de Compras** basado en comportamiento de clientes recurrentes.

---

## Estructura del proyecto

```
.
├── lambda_transformacion/      # Lógica de la Lambda con Dockerfile
│   ├── Dockerfile              # Dockerfile para el despliegue
│   ├── lambda_function.py      # Lógica a desplegar en la lambda
│   └── requirements.txt        # Requirements para la lambda
│
├── modelo_recomendacion/       # Desarrollo del modelo de predicción y recomendación
│   ├── output/, reports/, ...  # Archivos de salida
│   ├── src/                    # Código fuente
│   │   ├── data/               # Carga de datos
│   │   ├── features/           # Feature engineering
│   │   ├── models/             # Entrenamiento, predicción y recomendación
│   │   ├── evaluation/         # Métricas del modelo
│   │   └── utils/              # Utilidades comunes
│   ├── train_model.py          # Entrena y guarda el modelo
│   ├── predict_model.py        # Usa el modelo para predecir y recomendar
│   └── requirements.txt        # Requirements para el modelo de predicción
│
├── pyproject.toml              # Configuración de black, ruff, mypy
├── .pre-commit-config.yaml     # Hooks de pre-commit
├── Makefile                    # Comandos de desarrollo automatizados
├── requirements.txt            # Requirements para administración del repositorio (Linting)
└── README.md
```

---

## ETL en AWS Lambda

### Objetivo

Leer datos crudos desde un bucket S3 y generar un archivo limpio en formato `.parquet`, filtrando únicamente los **clientes recurrentes** según la siguiente definición:

> Clientes que compran al menos una vez cada 30 días, con más de 10 productos por compra.

### Tecnologías

- AWS Lambda Dockerizada
- Python 3.12
- Pandas + Boto3
- `.env` para credenciales y configuración

### Resultado

Un archivo `.parquet` limpio con solo clientes recurrentes, guardado en S3.

---

## Recomendador de Compras

### Objetivo

Predecir si un cliente comprará en una fecha futura específica y recomendarle sus 3 productos más frecuentes.

### Proceso

1. **Carga y preprocesamiento:** lectura desde S3, agregación diaria de compras.
2. **Calendario diario:** generación de días sin compra para cada usuario (comportamiento negativo).
3. **Feature engineering:**
   - Días desde última compra
   - Día de la semana, mes, día del mes
4. **Entrenamiento temporal:** split cronológico 80/20 con `XGBClassifier`
5. **Evaluación:** se imprime `classification_report` y `AUC`
6. **Predicción futura:** se calcula la probabilidad de recompra para una fecha futura.
7. **Recomendaciones:** se asignan los top-3 productos históricos por usuario.

### Scripts principales

- `train_model.py`: entrena el modelo y lo guarda en `models/model.pkl`
- `predict_model.py`: carga el modelo y predice para una fecha definida en el script

---

## Instalación y uso

Dentro de la carpeta modelo_recomendacion:

```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno
venv\Scripts\activate # Windows
source venv/bin/activat # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Entrenar modelo
python train_model.py

# Predecir para fecha futura
python predict_model.py
```

---

## Calidad y Estilo

Este repositorio usa las siguientes herramientas:

| Herramienta  | Propósito                      |
| ------------ | ------------------------------ |
| `ruff`       | Linter rápido y autofixer      |
| `black`      | Formateador de código          |
| `mypy`       | Verificador de tipos estáticos |
| `pre-commit` | Automatiza revisiones          |

---

## Requisitos

- Python 3.12+
- Docker (para probar Lambda local)

---

## Pruebas y Extensión futura

- [ ] Mejorar el modelo de predicción buscando más variables que brinden mayor información sobre los clientes
- [ ] Corrección de la columna precio en los datos iniciales, podría ser considerada a la hora de predecir futuras compras
- [ ] Automatizar backtesting para verificar constantemente la eficiencia del modelo
- [ ] Automatizar entrenamiento del módelo de recomendación con DAG o Lambda
- [ ] Crear API REST con FastAPI para exponer el modelo
- [ ] Integrar CI/CD (GitHub Actions)
