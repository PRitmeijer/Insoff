from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from charts.models import *
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from insoff.apps.charts.logic.bsdex import get_bsdex


# Create your views here.
def home(request):
    return render(request, 'base.html')


def charts(request):
    return render(request, 'portal/dashboard.html')

#Investment Calculator
class ChartIC(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'charts/ic.html'

    def get(self, request):
        assets = Asset.objects.all()
        return Response({'assets':assets})

#BuySell Index
class ChartBS(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'charts/bsindex.html'

    def get(self, request):
        assets = Asset.objects.all()
        return Response({'assets':assets})

class ChartBSData(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        from_date = datetime.strptime(request.POST.get('from_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        print(from_date)
        print(to_date)
        asset = request.POST.get('asset')
        scope = int(request.POST.get('scope'))
        pricedata = request.POST.get('pricedata')
        result = get_bsdex(asset, from_date, to_date, scope, pricedata)
        return Response(status=200, data=result)