from django.shortcuts import render
from django.http import HttpResponse
from listings.choices import bedrooms_choice, state_choice, price_choice
# Create your views here.
from listings.models import Listing
from realtors.models import Realtor
def index(request):
    Listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {
        'listings':Listings,
        'bedrooms_choice':bedrooms_choice,
        'state_choice':state_choice,
        'price_choice':price_choice
    }
    
    return render(request,'pages/index.html',context)

def about(request):
    realtors = Realtor.objects.order_by('-hire_date')
    # get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors':realtors,
        'mvp_realtors':mvp_realtors
    }
    return render(request,'pages/about.html',context)