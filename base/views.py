from django.shortcuts import render
from django.http import HttpResponse

import os
import pandas as pd
from django.conf import settings

def home(request):
    return render(request, "home.html")

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        print("file uploaded")

        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)

        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
       

        return render(request, "home.html")
    return render(request, "home.html")

#def get_locations(request):
#      uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
#     file_path = os.path.join(uploads_dir, filename)
    