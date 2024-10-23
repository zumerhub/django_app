from imp import reload
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Listing
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter

def main_view(request):
    return render(request, 'views/main.html', {"name": "AutoMax!!"})


@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    context = {
        'listing_filter': listing_filter
    }
    return render(request, 'views/home.html', context)

@login_required
def list_view(request):
    if request.method == "POST":
       try:
           listing_form = ListingForm(request.POST, request.FILES)
           location_form = LocationForm(request.POST)
           if listing_form.is_valid() and location_form.is_valid():
               listing = listing_form.save(commit=False)
               listing_location = location_form.save()
               listing.seller = request.user.profile
               listing.location = listing_location
               listing.save()
               messages.info(request, f"{listing.model} Listing created successfully.")
               return redirect('home')
           else:
               raise Exception(request, "Please complete the form.")
       except Exception as e:
           print(e)
           messages.error(request, "An error occurred while trying to create listing.")
    elif request.method == "GET":
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html',  {"listing_form": listing_form, "location_form": location_form })

def listing_view(request, id):
        try:
            listing = Listing.objects.get(id=id)
            if listing is None:
                raise Exception
            return render(request, 'views/listing.html', {"listing": listing})
            
        except Exception as e:
            print(e)
            messages.error(request, f"Invalid UID {id} was provided for listing.")
        return redirect('home')


@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        
        if request.method == 'POST':
            listing_form = ListingForm(request.POST, request.FILES, instance=listing)
            location_form = LocationForm(request.POST, instance=listing.location)
            
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
               messages.error(request, f"An error occurred while trying to edit the listing")
               return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
        
        context = {
            'listing_form': listing_form,
            'location_form': location_form 
        }
        return render(request, 'views/edit.html', context)
        
    except Exception as e:
        messages.error(request, 'An error occurred while trying to access the edit page.')
        return redirect('home')

