from django.shortcuts import render
from django.http import HttpResponse

import os
import pandas as pd
from django.conf import settings
import json
from django.shortcuts import render, redirect


def home(request):
    return render(request, "home.html")

def save_markers_to_json(data, json_file_path):
    markers = data[['store_no', 'latitude', 'longitude']].to_dict(orient='records')
    
    with open(json_file_path, 'w') as f:
        json.dump(markers, f)

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        print("file uploaded")

        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        data = pd.read_feather(file_path)
        print(data.columns)  # print the first 5 rows of the dataframe

        required_columns = {'store_no', 'latitude', 'longitude'}
        if not required_columns.issubset(data.columns):
            return HttpResponse("Uploaded file does not have the required columns: 'store_no', 'latitude', 'longitude'", status=400)

        json_file_path = os.path.join(settings.MEDIA_ROOT, 'markers.json')

        save_markers_to_json(data, json_file_path)

        return render(request, "home.html")
    return render(request, "home.html")


def predict(request):
    print("Predict !!!!!")
    print(request.method)
    if request.method == 'POST':
        model_choice = request.POST.get('modelSelect')  
        date_choice = request.POST.get('dateSelect')
        if model_choice == 'RF':
            print("Model 1 selected")
    return render(request, "predictpage.html")

def next_page(request):
    return render(request, "predictpage.html")
