# Network Security Anomaly Detection

End-to-end phishing URL classification pipeline: local CSV or MongoDB ingestion, schema validation and drift reporting, feature preprocessing, and a Random Forest classifier. The target column is `Result` (?1 indicates phishing and 1 indicates legitimate in the included dataset).

## Run locally

Python 3.10+ is recommended. Install dependencies and run:

```powershell
pip install -r requirements.txt
python main.py
```

When `MONGO_URL` is unset, the pipeline reads `Network_data/phisingData.csv`. To ingest MongoDB instead, set `MONGO_URL` in `.env`; the configured database and collection are in `network_Security/constants/training_pipeline/__init__.py`. Each run writes timestamped ingestion, validation, transformation, drift report, and model artifacts under `Artifacts/`. The serialized model bundle contains the estimator, preprocessor, and feature names.

## Data

The CSV must contain the columns listed in `data_schema/schema.yaml`, including `Result`. The pipeline uses a reproducible 80/20 train/test split. Test accuracy and weighted F1 are included in the printed model artifact.


## Frontend

Launch the interactive dashboard after training a model:

```powershell
streamlit run app.py
```

The dashboard supports a guided single-profile check and CSV batch scoring. Download the CSV template from the Batch Scan tab. Inputs must be the engineered features used by this model; it does not extract features by crawling arbitrary URLs.


## Connect MongoDB Atlas

1. In Atlas, create a database user and allow your current IP address under **Network Access**.
2. Copy the Atlas application connection string and set `MONGO_URL` in the project-root `.env` file (never commit this file):

   ```dotenv
   MONGO_URL=mongodb+srv://<db-user>:<url-encoded-password>@<cluster-host>/?retryWrites=true&w=majority&appName=NetworkSecurity
   ```

   Replace the placeholders with the Atlas values. URL-encode special characters in the password. The application reads database `first` and collection `NetworkData` (see `network_Security/constants/training_pipeline/__init__.py`).
3. Install dependencies with `pip install -r requirements.txt`, then verify access with `python test_mongo.py`.
4. Run `python main.py` to train from MongoDB, or `python push_data.py` to load `Network_data/phisingData.csv` into that database and collection.

The ingestion component falls back to the bundled CSV if a MongoDB connection fails. Run the connection check first when you need to confirm training is using MongoDB.
