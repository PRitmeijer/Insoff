from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from assets.models import *
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from insoff.apps.charts.logic.bsdex import get_bsdex
from insoff.apps.charts.logic.ic import get_investmentgraph


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

class ChartICData(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        from_date = datetime.strptime(request.POST.get('from_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
        print(from_date)
        print(to_date)
        asset = request.POST.get('asset')
        purchase_amount = int(request.POST.get('purchase_amount'))
        interval = int(request.POST.get('interval'))
        pricedata = request.POST.get('pricedata')
        result = get_investmentgraph(asset, from_date, to_date, purchase_amount, interval, pricedata)
        return Response(status=200, data=result)

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