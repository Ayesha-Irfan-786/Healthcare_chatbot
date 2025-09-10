import pandas as pd

# ---------------------------
# Load datasets
# ---------------------------
data = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\dataset.csv")
desc = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\symptom_Description.csv")
precaution = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\symptom_precaution.csv")
severity = pd.read_csv("C:\\Users\\Izza Traders\\Desktop\\Healthcare_chatbot\\dataset\\Symptom-severity.csv")

# ---------------------------
# Preprocessing: Handle NaN
# ---------------------------
# Replace NaN values with empty strings
data = data.fillna("")
desc = desc.fillna("")
precaution = precaution.fillna("")
severity = severity.fillna("")

print("Main Data:", data.head())
print("Descriptions:", desc.head())
print("Precautions:", precaution.head())
print("Severity:", severity.head())


# ---------------------------
# Normalize function
# ---------------------------
def normalize_symptom(symptom):
    return symptom.strip().lower().replace(" ", "_")


# Function to predict disease based on symptom input
def predict_disease(user_symptoms):
    # Normalize user input
    symptoms = [normalize_symptom(s) for s in user_symptoms.split(",")]

    # Search in dataset for disease matching symptoms
    for i, row in data.iterrows():
        # Normalize dataset symptoms (skip empty ones)
        disease_symptoms = [
            normalize_symptom(str(row[col])) 
            for col in data.columns 
            if "Symptom" in col and row[col] != ""
        ]

        # Check if user symptoms exist in the disease symptoms list
        if any(symptom in disease_symptoms for symptom in symptoms):
            disease = row["Disease"]

            # Get description
            description = desc[desc["Disease"] == disease]["Description"].values
            description = description[0] if len(description) > 0 else "No description available."

            # Get precautions
            precautions = precaution[precaution["Disease"] == disease].iloc[:, 1:].values
            if len(precautions) > 0:
                precautions = ", ".join([p for p in precautions[0] if str(p) != ""])
            else:
                precautions = "No precautions available."

            return f"Disease: {disease}\nDescription: {description}\nPrecautions: {precautions}"

    return "Sorry, I couldn't find a matching disease."


# ---------------------------
# Simple chatbot loop
# ---------------------------
while True:
    user_input = input("Enter your symptoms separated by commas (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    print(predict_disease(user_input))
