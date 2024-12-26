from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from datetime import datetime

@csrf_protect
def predict(request):
    if request.method == 'POST':
        prediction_date = request.POST.get('prediction_date')
        model_type = request.POST.get('model_type')
        
        # Convert string date to datetime object
        prediction_date = datetime.strptime(prediction_date, '%Y-%m-%d')
        
        # Here you can add your model prediction logic based on the selected model_type
        # For now, we'll just return the received data
        response_data = {
            'prediction_date': prediction_date.strftime('%Y-%m-%d'),
            'model_type': model_type,
            'status': 'success'
        }
        
        return JsonResponse(response_data)
    
    return render(request, 'selection.html')
