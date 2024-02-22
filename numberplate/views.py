from django.http import JsonResponse
from .models import TrespassingEvent, Deal, Thread, ThreadImage, AccessToken, LicencePlates
import json
from django.contrib import messages
import logging
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from datetime import datetime

logger = logging.getLogger(__name__)

def extract_trespassing_info(json_data):
    trespassing_info = []
    for event in json_data.get("trespassing_events", []):
        datetime_str = event.get("datetime")
        formatted_datetime = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")

        info = {
            "license_plate": event.get("license_plate"),
            "datetime_of_trespassing": formatted_datetime,
            "image_url": event.get("image_url"),
            "location": event.get("location")
        }
        trespassing_info.append(info)
    return trespassing_info

@csrf_exempt
def save_trespassing_info(request):
    if request.method == 'POST':
        try:
            activation_key = request.headers.get('Authorization')
            try:
                access_token = AccessToken.objects.get(access_token=activation_key)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Invalid activation key'}, status=401)
            
            data = json.loads(request.body)
            trespassing_info = extract_trespassing_info(data)
            
            for info in trespassing_info:
                license_plate_number = info['license_plate']
                datetime_of_trespassing = info['datetime_of_trespassing']
                image_url = info.get('image_url') 
                location = info['location']

                license_plate, created = LicencePlates.objects.get_or_create(plate_number=license_plate_number)
                trespassing_event = TrespassingEvent.objects.create(
                    license_plate=license_plate,
                    datetime_of_trespassing=datetime_of_trespassing,
                    location=location,
                    image_url=image_url
                )

                thread_info = f"Trespassing event recorded on {datetime_of_trespassing} at {location}."
                thread, thread_created = Thread.objects.update_or_create(
                    license_plate=license_plate,
                    defaults={'thread_info': thread_info}
                )
                thread_image, thread_image_created = ThreadImage.objects.get_or_create(thread=thread)
                if not thread_image_created:
                    thread_image.image_url = image_url
                    thread_image.save()

            return JsonResponse({'message': 'Trespassing events saved successfully'}, status=201)
        except Exception as e:
            logger.exception("An error occurred while saving trespassing events:")
            return JsonResponse({'error': 'An error occurred while saving trespassing events. Please check the logs for more information.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account created successfully. You are now logged in.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Failed to authenticate user after signup.')
        else:
            messages.error(request, 'Form is not valid. Please check your input.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  

def dashboard(request):
    return render(request, 'dashboard.html')
