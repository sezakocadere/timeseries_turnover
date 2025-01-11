from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
import pandas as pd
from django.conf import settings
import json
from django.shortcuts import render, redirect
import joblib
from datetime import datetime, timedelta
import numpy as np
import openpyxl
import logging

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'random_forest_best_model.pkl')

def load_model():
    try:        
        if not os.path.exists(MODEL_PATH):
            error_msg = f"NOT FOUND MODEL {MODEL_PATH}"
            raise FileNotFoundError(error_msg)
            
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        error_msg = f"Model load error: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

def prepare_features(date_str, store_no=None):
    try:
        start_date = datetime.strptime(date_str, '%Y-%m-%d')
        dates = [start_date + timedelta(days=x) for x in range(14)]
        
        features = []
        for d in dates:
            store_no_int = int(store_no) if store_no else 101
            
            store_features = {
                'store_no': store_no_int,
                'date': d,
                'day': d.day,
                'month': d.month,
                'year': d.year,
                'dayofweek': d.weekday()
            }
            features.append(store_features)
        
        df = pd.DataFrame(features)
        return df
        
    except Exception as e:
        logging.error(f"Error preparing features: {str(e)}")
        raise e

def predict_turnover(store_data):
    features = store_data[['store_no', 'day', 'month', 'year', 'dayofweek']].copy()
    
    model = load_model()
    predictions = model.predict(features)
    
    results = store_data[['store_no', 'date']].copy()
    results['predicted_turnover'] = predictions
    return results

def save_markers_to_json(data, json_file_path):
    markers = data[['store_no', 'latitude', 'longitude']].to_dict(orient='records')
    with open(json_file_path, 'w') as f:
        json.dump(markers, f)

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        logging.info("File uploaded")

        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        data = pd.read_feather(file_path)
        required_columns = {'store_no', 'latitude', 'longitude'}
        if not required_columns.issubset(data.columns):
            return HttpResponse("Uploaded file does not have the required columns: 'store_no', 'latitude', 'longitude'", status=400)

        json_file_path = os.path.join(settings.MEDIA_ROOT, 'markers.json')
        save_markers_to_json(data, json_file_path)

        return render(request, "home.html")
    return render(request, "home.html")

def predict(request):
    context = {}
    
    if request.method == 'POST':
        model_choice = request.POST.get('modelSelect')
        date_choice = request.POST.get('dateSelect')
        store_no = request.POST.get('store_no')
                
        if date_choice and model_choice == 'RF' and store_no:
            try:
                request.session['selected_date'] = date_choice
                store_data = prepare_features(date_choice, store_no)
                predictions = predict_turnover(store_data)
                
                prediction_list = []
                for _, row in predictions.iterrows():
                    prediction_list.append((
                        row['date'].strftime('%Y-%m-%d'),
                        round(float(row['predicted_turnover']), 2)
                    ))
                
                context['predictions'] = prediction_list
                context['selected_date'] = date_choice
                context['selected_model'] = model_choice
                context['selected_store_no'] = store_no
                
            except Exception as e:
                error_msg = f"Prediction error: {str(e)}"
                logging.error(error_msg)
                context['error'] = error_msg
        else:
            context['error'] = "Select store number"
    
    return render(request, "predictpage.html", context)

def download_all_predictions(request):
    try:
        model_choice = request.GET.get('model', 'RF')
        date_choice = request.session.get('selected_date')
        if not date_choice:
            return HttpResponse("Choose a date", status=400)
            
        if model_choice != 'RF':
            return HttpResponse("Just RF model", status=400)
        
        try:
            feather_files = [f for f in os.listdir(settings.MEDIA_ROOT) if f.endswith('.feather')]
            if not feather_files:
                return HttpResponse("Not found Dataset", status=400)
            
            data = pd.read_feather(os.path.join(settings.MEDIA_ROOT, feather_files[0]))
            unique_stores = sorted(data['store_no'].unique())
            
            if not unique_stores:
                return HttpResponse("Can not found store number in dataset", status=400)
        except Exception as e:
            error_msg = f"Dataset reading error: {str(e)}"
            logging.error(error_msg)
            return HttpResponse(error_msg, status=500)
        
        all_predictions = []
        
        for store_no in unique_stores:
            store_data = prepare_features(date_choice, store_no)
            predictions = predict_turnover(store_data)
            
            for _, row in predictions.iterrows():
                all_predictions.append({
                    'Store_No': row['store_no'],
                    'Date': row['date'].strftime('%Y-%m-%d'),
                    'Predicted_Turnover': round(float(row['predicted_turnover']), 2)
                })
        
        df = pd.DataFrame(all_predictions)        
        df = df.sort_values(['Store_No', 'Date'])
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=store_predictions.xlsx'
        
        with pd.ExcelWriter(path=response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Predictions')
            
            worksheet = writer.sheets['Predictions']
            worksheet.column_dimensions['A'].width = 15  # Store_No
            worksheet.column_dimensions['B'].width = 20  # Date
            worksheet.column_dimensions['C'].width = 25  # Predicted_Turnover
            
            for cell in worksheet[1]:
                cell.font = openpyxl.styles.Font(bold=True)
            
            for row in worksheet.iter_rows(min_row=2, min_col=3, max_col=3):
                for cell in row:
                    cell.number_format = '#,##0.00'
                    cell.alignment = openpyxl.styles.Alignment(horizontal='right')
        
        return response
    except Exception as e:
        error_msg = f"Creating Excel Error: {str(e)}"
        logging.error(error_msg)
        return HttpResponse(error_msg, status=500)

def get_store_predictions(request):
    try:
        store_no = request.GET.get('store_no')
        if not store_no:
            return JsonResponse({'error': 'Store number is required'}, status=400)
            
        current_date = datetime.now().strftime('%Y-%m-%d')
        store_data = prepare_features(current_date, store_no)
        results = predict_turnover(store_data)
        
        predictions = []
        for _, row in results.iterrows():
            predictions.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'turnover': float(row['predicted_turnover'])
            })
            
        return JsonResponse({
            'store_no': store_no,
            'predictions': predictions
        })
        
    except Exception as e:
        logging.error(f"Error getting store predictions: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def next_page(request):
    return render(request, "map.html")

def home(request):
    return render(request, "home.html")