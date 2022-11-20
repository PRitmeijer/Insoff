from django.urls import path, include
from charts import views


urlpatterns = [
    path('api/chartview', views.ChartOverview.as_view(), name='api_chart_overview'),
    path('api/raw_data', views.ChartData.as_view(), name='api_raw_data'),
]