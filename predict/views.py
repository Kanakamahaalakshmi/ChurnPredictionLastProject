# predict/views.py
from django.shortcuts import render
import joblib  # or pickle, depending on your model

# Load your trained model
model = joblib.load("path/to/your/model.pkl")

def predict_churn(request):
    if request.method == "POST":
        feature1 = float(request.POST["feature1"])
        feature2 = float(request.POST["feature2"])
        feature3 = float(request.POST["feature3"])
        
        # Convert input to model format
        input_data = [[feature1, feature2, feature3]]
        prediction = model.predict(input_data)[0]  # Get prediction

        return render(request, "index.html", {"prediction": prediction})
    
    return render(request, "index.html")

