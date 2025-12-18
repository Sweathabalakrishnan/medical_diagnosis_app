import pandas as pd
import json

df = pd.read_csv("datasets/Training.csv")

diseases = sorted(df["prognosis"].unique())

disease_index = {str(i): disease for i, disease in enumerate(diseases)}

with open("diseases.json", "w") as f:
    json.dump(disease_index, f, indent=4)

print(len(disease_index))  # MUST be 41
