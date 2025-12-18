import pandas as pd
import json
import os

CSV_FILES = {
    "description":"datasets/description.csv",
    "symptoms": "datasets/symtoms_df.csv",
    "precautions": "datasets/precautions_df.csv",
    "medications": "datasets/medications.csv",
    "diets": "datasets/diets.csv",
    "workout": "datasets/workout_df.csv"
}

os.makedirs("json", exist_ok=True)

for name, path in CSV_FILES.items():
    df = pd.read_csv(path)
    df.to_json(f"json/{name}.json", orient="records", indent=4)

print("✅ All CSV files converted to JSON successfully")
