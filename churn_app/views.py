import os
import joblib
import numpy as np
import csv
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import ChurnPrediction  # Ensure this model exists in models.py

# ✅ Export churn predictions to CSV
def export_churn_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="churn_predictions.csv"'

    writer = csv.writer(response)
    writer.writerow(["Customer ID", "Tenure", "Monthly Charges", "Total Charges", "Prediction"])

    churn_data = ChurnPrediction.objects.all().values_list(
        "customer_id", "tenure", "monthly_charges", "total_charges", "prediction"
    )
    for data in churn_data:
        writer.writerow(data)

    return response

# ✅ Home Page View
def home(request):
    return render(request, "index.html")  # Ensure 'index.html' exists in your templates folder

# ✅ Load Model Path
model_path = os.path.join(settings.BASE_DIR, "churn_app", "best_model.pkl")

# ✅ Load the Model if File Exists
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print(f"⚠️ Error: Model file not found at {model_path}")

# ✅ Prediction View
def make_prediction(request):
    if request.method == "POST":
        if not model:
            return JsonResponse({"error": "⚠️ Model file is missing."}, status=400)

        try:
            # 🛠 Ensure form fields match EXACTLY with the index.html input names
            features = [
                float(request.POST.get("tenure", 0)),
                float(request.POST.get("MonthlyCharges", 0)),  # Ensure correct field names
                float(request.POST.get("TotalCharges", 0)),
                float(request.POST.get("TenureGroup", 0)),
                float(request.POST.get("PhoneService_Yes", 0)),
                float(request.POST.get("Contract_One year", 0)),  # Fix field names
                float(request.POST.get("Contract_Two year", 0)),
                float(request.POST.get("PaperlessBilling_Yes", 0)),
                float(request.POST.get("PaymentMethod_Credit card (automatic)", 0)),  # Fix
                float(request.POST.get("Churn_Yes", 0)),
            ]

            # Convert to model input format
            user_input = np.array([features])

            # Predict churn (1 = Churn, 0 = No Churn)
            prediction = model.predict(user_input)[0]
            result = "❌ The customer is likely to CHURN" if prediction == 1 else "✅ The customer is likely to STAY"

            # Render the results page with the prediction
            return render(request, "result.html", {"prediction": result})

        except Exception as e:
            return JsonResponse({"error": f"❌ Prediction failed: {str(e)}"}, status=400)

    return JsonResponse({"error": "⚠️ Invalid request method."}, status=400)


