from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def line_webhook(request):
    return HttpResponse("OK", 200)
