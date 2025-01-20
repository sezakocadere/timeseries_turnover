from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.predict, name="predict"),
    path("download-all-predictions/", views.download_all_predictions, name="download-all-predictions"),
    path('get_store_predictions/', views.get_store_predictions, name='get_store_predictions'),
    path('download-store-predictions/', views.download_store_predictions, name='download-store-predictions'),
    path('get_model_comparison/', views.get_model_comparison, name='get_model_comparison'),
]
