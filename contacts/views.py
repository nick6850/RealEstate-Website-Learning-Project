from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
import passwords

# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this lising')
                return redirect('/listings/'+listing_id)


        Contact.objects.create(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)
        
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
            passwords.EMAIL_HOST_USER,
            [passwords.EMAIL_HOST_USER],
            fail_silently=False
        )
        
        
        messages.success(request, 'Your request has been submitted')
        return redirect('/listings/' + listing_id) 