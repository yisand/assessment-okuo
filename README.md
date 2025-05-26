
# 🛒 Recomendador de Compras + ETL Lambda

Este repositorio contiene dos componentes principales desarrollados para una prueba técnica de datos:

1. **ETL en AWS Lambda (Dockerizada)** que transforma los datos crudos desde S3.
2. **Modelo de Recomendación de Compras** basado en comportamiento de clientes recurrentes.

---

## 📁 Estructura del proyecto

```
.
├── lambda_transformacion/       # Lógica de la Lambda con Dockerfile
│   ├── Dockerfile
│   ├── lambda_function.py
│   └── requirements.txt
│
├── modelo_recomendacion/       # Desarrollo del modelo de predicción y recomendación
│   ├── notebooks/               # Notebooks exploratorios
│   ├── output/, reports/, ...  # Archivos de salida
│   ├── src/                    # Código fuente
│   │   ├── data/               # Carga de datos
│   │   ├── features/           # Feature engineering
│   │   ├── models/             # Entrenamiento, predicción y recomendación
│   │   ├── evaluation/         # Métricas del modelo
│   │   ├── pipeline/           # Orquestación
│   │   └── utils/              # Utilidades comunes
│   ├── train_model.py          # Entrena y guarda el modelo
│   ├── predict_model.py        # Usa el modelo para predecir y recomendar
│   └── requirements.txt
│
├── pyproject.toml              # Configuración de black, ruff, mypy
├── .pre-commit-config.yaml     # Hooks de pre-commit
├── Makefile                    # Comandos de desarrollo automatizados
└── README.md
```

---

## 🚀 Lambda ETL

### 🌐 Objetivo

Leer datos crudos desde un bucket S3 y generar un archivo limpio en formato `.parquet`, filtrando únicamente los **clientes recurrentes** según la siguiente definición:

> Clientes que compran al menos una vez cada 30 días, con más de 10 productos por compra, y cuya variabilidad (std) también sea baja.

### ⚙️ Tecnologías

- AWS Lambda Dockerizada
- Python 3.12
- Pandas + Boto3
- `.env` para credenciales y configuración

### ✅ Resultado

Un archivo `.parquet` limpio con solo clientes recurrentes, guardado en S3 o local para pruebas.

---

## 🤖 Recomendador de Compras

### 📊 Objetivo

Predecir si un cliente comprará en una fecha futura específica y recomendarle sus 3 productos más frecuentes.

### ⚙️ Proceso

1. **Carga y preprocesamiento:** Lectura desde S3, agregación diaria de compras.
2. **Calendario diario:** Generación de días sin compra para cada usuario (comportamiento negativo).
3. **Feature engineering:**
   - Días desde última compra
   - Día de la semana, mes, día del mes
4. **Entrenamiento temporal:** Split cronológico 80/20 con `XGBClassifier`
5. **Evaluación:** Se imprime `classification_report` y `AUC`
6. **Predicción futura:** Se calcula la probabilidad de recompra para una fecha futura.
7. **Recomendaciones:** Se asignan los top-3 productos históricos por usuario.

### ⚙️ Scripts principales

- `train_model.py`: Entrena el modelo y lo guarda en `models/model.pkl`
- `predict_model.py`: Carga el modelo y predice para una fecha definida en el script

---

## 🚀 Instalación y uso

```bash
# Crear entorno virtual
make venv

# Instalar dependencias
make install

# Instalar pre-commit y hooks
make install-precommit

# Entrenar modelo
python train_model.py

# Predecir para fecha futura
python predict_model.py
```

---

## 🌐 Calidad y estilo

Este repo usa las siguientes herramientas:

| Herramienta  | Propósito                      |
| ------------ | ------------------------------ |
| `ruff`       | Linter rápido y autofixer      |
| `black`      | Formateador de código          |
| `mypy`       | Verificador de tipos estáticos |
| `pre-commit` | Automatiza revisiones          |

Ejecuta todo con:

```bash
make check-all
```

---

## 📦 Requisitos

- Python 3.12+
- AWS CLI configurado si se desea usar S3
- Docker (para probar Lambda local)

---

## 🧪 Pruebas y extensión futura

- [ ] Automatizar entrenamiento con DAG o Lambda
- [ ] Crear API REST con FastAPI para exponer el modelo
- [ ] Integrar CI/CD (GitHub Actions)

---

## 📬 Contacto

Este repo fue desarrollado para una prueba técnica como ejercicio integral de ETL + ML + buenas prácticas.
