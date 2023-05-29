from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save-data/', views.save_data, name='save_data'),
    path('predict-failure/', views.predict_failure, name='predict_failure'),
    path('check-prediction/', views.check_prediction, name='check_prediction'),  # New URL mapping
]
