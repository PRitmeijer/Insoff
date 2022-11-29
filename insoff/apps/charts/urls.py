from django.urls import path, include
from charts import views


urlpatterns = [
    path('api/chartview/ic', views.ChartIC.as_view(), name='api_chart_ic'),
    path('api/ic/data', views.ChartBSData.as_view(), name='api_chart_ic_data'),
    path('api/chartview/bsindex', views.ChartBS.as_view(), name='api_chart_bsindex'),
    path('api/bs/data', views.ChartBSData.as_view(), name='api_chart_bsindex_data'),
]