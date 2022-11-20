from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from charts.models import *
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    return render(request, 'base.html')


def charts(request):
    return render(request, 'portal/dashboard.html')


class ChartOverview(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'charts/charts.html'

    def get(self, request):
        assets = Asset.objects.all()
        return Response({'assets':assets})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        from_date = datetime.strptime(request.POST.get('from_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        asset = request.POST.get('asset')
        interval = request.POST.get('interval')
        stats = PriceStat.objects.filter(
            asset_id = asset,
            date__gte = from_date,
            date__lte = to_date,
            interval = interval
        ).order_by('-date')
        if stats is not None:
            data = [{
                'date':s.date,
                'vwap':s.vwap
            } for s in stats]
            return Response(status=200, data=data)
        else:
            return Response(status=204)