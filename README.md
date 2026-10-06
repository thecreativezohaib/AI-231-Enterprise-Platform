# AI-231 Enterprise Autonomous Infrastructure Intelligence

## Overview
This is the completed source code for the 6-week AI-231 Enterprise Platform.

## Architecture
- **Backend:** Python FastAPI
- **Databases:** PostgreSQL (Relational Assets), Neo4j (Knowledge Graph), Redis (Caching)
- **Streaming:** Apache Kafka
- **AI/ML:** Scikit-Learn (Anomaly Detection), LLM (Copilot)
- **Frontend:** Streamlit Executive Dashboard

## Project Structure
```
Project 2/
├── docker-compose.yml          # Core Infrastructure (Postgres, Neo4j, Redis, Kafka)
├── backend/
│   ├── main.py                 # FastAPI Entrypoint
│   ├── requirements.txt        # Python Dependencies
│   ├── ingestion_worker.py     # Kafka Consumer & ML Inference
│   ├── api/                    # REST Endpoints (assets.py, copilot.py)
│   ├── core/                   # DB Connections & ML Models (database.py, ml_models.py, rca_engine.py)
│   ├── data_simulator/         # Mock IoT telemetry generator
│   └── models/                 # SQLAlchemy DB schemas
└── dashboard/
    └── app.py                  # Streamlit UI
```

## How to Run Locally

### 1. Start Infrastructure
```bash
docker-compose up -d
```

### 2. Setup Python Environment
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the Backend API
```bash
uvicorn backend.main:app --reload
```

### 4. Run the Data Simulator and AI Worker
In separate terminals:
```bash
python backend/data_simulator/simulator.py
python backend/ingestion_worker.py
```

### 5. Launch the Dashboard
```bash
streamlit run dashboard/app.py
```
