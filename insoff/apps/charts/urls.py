from django.urls import path, include
from charts import views


urlpatterns = [
    path('api/raw_data', views.ChartData.as_view(), name='api_raw_data'),
]