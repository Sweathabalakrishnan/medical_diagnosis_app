# from flask import Flask, render_template, request
# import numpy as np
# import pickle
# import json

# app = Flask(__name__)

# # ---------------- LOAD MODEL ----------------
# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

# # ---------------- LOAD SYMPTOM INDEX (132 FEATURES) ----------------
# with open("symptom_index.json", "r", encoding="utf-8") as f:
#     symptom_index = json.load(f)

# # ---------------- LOAD DISEASE LABELS (41 CLASSES) ----------------
# with open("diseases.json", "r", encoding="utf-8") as f:
#     diseases = json.load(f)

# # ---------------- HELPER: CLEAN + REMOVE DUPLICATES ----------------
# def clean_unique_list(items):
#     seen = set()
#     cleaned = []
#     for item in items:
#         if isinstance(item, str):
#             item = item.strip()
#             if item and item.lower() not in seen:
#                 cleaned.append(item)
#                 seen.add(item.lower())
#     return cleaned

# # ---------------- HELPER: LOAD MEDICAL JSON FILES ----------------
# def load_list_json(path):
#     with open(path, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     result = {}

#     for item in data:
#         disease = item.get("Disease") or item.get("disease")
#         if not disease:
#             continue

#         key = str(disease).lower()
#         values = []

#         for k, v in item.items():
#             if k.lower() in ["disease", "unnamed: 0"]:
#                 continue

#             if isinstance(v, str) and v.strip():
#                 values.append(v.strip())

#             elif isinstance(v, list):
#                 values.extend([x.strip() for x in v if isinstance(x, str)])

#         result[key] = clean_unique_list(values)

#     return result

# # ---------------- LOAD MEDICAL DATA ----------------
# description = load_list_json("data/description.json")
# precautions = load_list_json("data/precautions.json")
# medications = load_list_json("data/medications.json")
# diets = load_list_json("data/diets.json")
# workout = load_list_json("data/workout.json")

# # ---------------- HOME ROUTE ----------------
# @app.route("/", methods=["GET"])
# def home():
#     return render_template(
#         "index.html",
#         symptoms=sorted(symptom_index.keys())
#     )

# # ---------------- PREDICT ROUTE ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     selected_symptoms = request.form.getlist("symptoms")

#     # Create 132-feature input vector
#     input_vector = np.zeros(len(symptom_index))

#     for symptom in selected_symptoms:
#         symptom = symptom.strip().lower()
#         if symptom in symptom_index:
#             input_vector[symptom_index[symptom]] = 1

#     # ---------- MODEL PREDICTION ----------
#     prediction = int(model.predict([input_vector])[0])

#     # Safe disease lookup
#     disease = diseases.get(str(prediction), "Unknown Disease")
#     disease = str(disease)
#     key = disease.lower()
    

    
#     # ---------- CONFIDENCE SCORE ----------
#     confidence = None
#     if hasattr(model, "predict_proba"):
#         probabilities = model.predict_proba([input_vector])[0]
#         confidence = round(float(np.max(probabilities)) * 100, 2)

#     return render_template(
#         "index.html",
#         symptoms=sorted(symptom_index.keys()),
#         disease=disease,
#         confidence=confidence,
#         description=", ".join(description.get(key, ["No description available"])),
#         precautions=precautions.get(key, ["No precautions available"]),
#         medications=medications.get(key, ["No medications available"]),
#         diets=diets.get(key, ["No diet recommendations"]),
#         workout=workout.get(key, ["No workout suggestions"])
#     )

# # ---------------- RUN APPLICATION ----------------
# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, render_template, request
import numpy as np
import pickle
import json

app = Flask(__name__)

# ---------------- LOAD MODEL ----------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------- LOAD SYMPTOM INDEX (132 FEATURES) ----------------
with open("symptom_index.json", "r", encoding="utf-8") as f:
    symptom_index = json.load(f)

# ---------------- LOAD DISEASE LABELS (41 CLASSES) ----------------
with open("diseases.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

# ---------------- HELPER: CLEAN + REMOVE DUPLICATES ----------------
def clean_unique_list(items):
    seen = set()
    cleaned = []
    for item in items:
        if isinstance(item, str):
            item = item.strip()
            if item and item.lower() not in seen:
                cleaned.append(item)
                seen.add(item.lower())
    return cleaned

# ---------------- HELPER: LOAD MEDICAL JSON FILES ----------------
def load_list_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = {}

    for item in data:
        disease = item.get("Disease") or item.get("disease")
        if not disease:
            continue

        key = str(disease).lower()
        values = []

        for k, v in item.items():
            if k.lower() in ["disease", "unnamed: 0"]:
                continue

            if isinstance(v, str) and v.strip():
                values.append(v.strip())

            elif isinstance(v, list):
                values.extend([x.strip() for x in v if isinstance(x, str)])

        result[key] = clean_unique_list(values)

    return result

# ---------------- LOAD MEDICAL DATA ----------------
description = load_list_json("data/description.json")
precautions = load_list_json("data/precautions.json")
medications = load_list_json("data/medications.json")
diets = load_list_json("data/diets.json")
workout = load_list_json("data/workout.json")

# ---------------- HOME ROUTE ----------------
@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        symptoms=sorted(symptom_index.keys())
    )

# ---------------- PREDICT ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    selected_symptoms = request.form.getlist("symptoms")

    # Create 132-feature input vector
    input_vector = np.zeros(len(symptom_index))

    for symptom in selected_symptoms:
        symptom = symptom.strip().lower()
        if symptom in symptom_index:
            input_vector[symptom_index[symptom]] = 1

    input_vector = input_vector.reshape(1, -1)

    # ---------- PREDICTION ----------
    prediction_idx = int(model.predict(input_vector)[0])
    disease = diseases.get(str(prediction_idx), "Unknown Disease")
    key = disease.lower()

    # ---------- CONFIDENCE + TOP-3 ----------
    confidence = None
    top3 = []

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_vector)[0]

        # Top 3 indices
        top3_idx = np.argsort(probs)[-3:][::-1]

        for i in top3_idx:
            top3.append({
                "disease": diseases.get(str(i), "Unknown"),
                "confidence": round(float(probs[i]) * 100, 2)
            })

        confidence = top3[0]["confidence"]

    return render_template(
        "index.html",
        symptoms=sorted(symptom_index.keys()),
        disease=disease,
        confidence=confidence,
        top3=top3,
        description=", ".join(description.get(key, ["No description available"])),
        precautions=precautions.get(key, ["No precautions available"]),
        medications=medications.get(key, ["No medications available"]),
        diets=diets.get(key, ["No diet recommendations"]),
        workout=workout.get(key, ["No workout suggestions"])
    )

# ---------------- RUN APPLICATION ----------------
if __name__ == "__main__":
    app.run(debug=True)
