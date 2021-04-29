from django.shortcuts import render, get_object_or_404

from listings.choices import bedrooms_choice,price_choice,state_choice
from django.core.paginator import EmptyPage, Paginator
from .models import Listing
# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings':paged_listings,
        
    }
    return render(request,'listings/listings.html',context=context)
    
def listing(request, listing_id):
    listing = get_object_or_404(Listing,pk = listing_id)

    context = {
        'listing':listing,
    }
    return render(request,'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = Listing.objects.filter(description__icontains = keywords)
    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = Listing.objects.filter(city__iexact = city)
    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = Listing.objects.filter(state__iexact = state)
    
    # bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = Listing.objects.filter(bedrooms__lte = bedrooms) # lte = less than equalto
    
    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = Listing.objects.filter(price__lte = price) # lte = less than equalto

    context = {
        'bedrooms_choice':bedrooms_choice,
        'price_choice':price_choice,
        'state_choice':state_choice,
        'listings':queryset_list,
        'values': request.GET,
        
    }

    return render(request,'listings/search.html',context)