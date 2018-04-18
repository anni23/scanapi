from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webapp import scanfile
class scanAPI(APIView):

    def get(self, request, file_name):
        data = scanfile.callScanAPI(file_name)
        return Response(data)
'''    
    def post(self, request):
        data = scanfile.callScanAPI(file_name)
        return Response(data)
'''