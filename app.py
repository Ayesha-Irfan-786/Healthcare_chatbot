from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# -----------------------------
# Load datasets
# -----------------------------
data = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\dataset.csv").fillna("")
desc = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\symptom_Description.csv").fillna("")
precaution = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\symptom_precaution.csv").fillna("")
severity = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\Symptom-severity.csv").fillna("")

# Clean NaN values
data.fillna("", inplace=True)
desc.fillna("", inplace=True)
precaution.fillna("", inplace=True)
severity.fillna("", inplace=True)

# -----------------------------
# Normalize function
# -----------------------------
def normalize_symptom(symptom):
    return symptom.strip().lower().replace(" ", "_")

# -----------------------------
# Prediction function
# -----------------------------
def predict_disease(user_symptoms):
    symptoms = [normalize_symptom(s) for s in user_symptoms.split(",")]

    for _, row in data.iterrows():
        disease_symptoms = [
            normalize_symptom(str(row[col]))
            for col in data.columns if "Symptom" in col and str(row[col]) != "nan"
        ]

        if any(symptom in disease_symptoms for symptom in symptoms):
            disease = row["Disease"]

            description = desc[desc["Disease"] == disease]["Description"].values
            description = description[0] if len(description) > 0 else "No description available."

            precautions = precaution[precaution["Disease"] == disease].iloc[:, 1:].values
            if len(precautions) > 0:
                precautions = ", ".join([p for p in precautions[0] if str(p) != "nan"])
            else:
                precautions = "No precautions available."

            return f"🦠 Disease: {disease}\n📖 {description}\n✅ Precautions: {precautions}"

    return "❌ Sorry, I couldn't find a matching disease."


# -----------------------------
# Greeting check
# -----------------------------
def check_greeting(message):
    greetings = ["hi", "hello", "hey", "salam", "hy", "hii"]
    if message.lower().strip() in greetings:
        return "👋 Hello! I’m your Healthcare Assistant.\nWhich symptoms would you like to ask about today?"
    return None


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_msg = request.form["msg"]

    # Check greetings first
    greet_response = check_greeting(user_msg)
    if greet_response:
        return jsonify({"reply": greet_response})

    # Otherwise, go to disease prediction
    bot_reply = predict_disease(user_msg)
    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)

