#!/bin/bash

echo "Iniciando la API (FastAPI)..."
python -m uvicorn app.main:app --reload --port 8001 &
API_PID=$!

echo "Iniciando la interfaz (Streamlit)..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

# Asegurarnos de que cuando presiones Ctrl+C, ambos procesos se cierren
trap "kill $API_PID $STREAMLIT_PID; echo 'Procesos detenidos.'" SIGINT SIGTERM EXIT

# Mantener el script en ejecución mientras esperamos que ambos procesos terminen
wait
