from django.shortcuts import HttpResponse 

def home_page(request):
    return HttpResponse('<html><title>Review Pictures</title></html>')

