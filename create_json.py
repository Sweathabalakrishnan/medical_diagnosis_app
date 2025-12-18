import json

# Paste your full symptoms_dict here
symptoms_dict = {
    'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3,
    'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8,
    'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12,
    'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16,
    # … include all 132 symptoms exactly as in your notebook
}

# Paste your full diseases_list here
diseases_list = {
    15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis',
    14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ',
    # … include all diseases exactly as in your notebook
}

# Save symptoms.json
with open("datasets/symptoms.json", "w") as f:
    json.dump(symptoms_dict, f)

# Save diseases.json
with open("datasets/diseases.json", "w") as f:
    json.dump(diseases_list, f)

print("✅ JSON files created successfully!")
