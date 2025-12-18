import pandas as pd
import json

df = pd.read_csv("datasets/Training.csv")

symptoms = list(df.columns)
symptoms.remove("prognosis")  # disease column

symptom_index = {symptom: i for i, symptom in enumerate(symptoms)}

with open("symptom_index.json", "w") as f:
    json.dump(symptom_index, f, indent=4)

print(len(symptom_index))  # MUST PRINT 132
