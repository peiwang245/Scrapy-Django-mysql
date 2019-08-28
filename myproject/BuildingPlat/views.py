from django.shortcuts import render
from django.http import HttpResponse
from .models import  CallBid, WinBid
import markdown
# Create your views here.

def home(request):
    bids = CallBid.objects.all()
    bids_names = list()
    for bid in bids:
        bids_names.append(bid.name)
    response_html ='<br>'.join(bids_names)#???
    return HttpResponse(response_html)


