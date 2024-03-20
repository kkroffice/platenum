# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import TrespassingEvent, Deal, Authorities, ThreadImage, WorkflowStep, LicencePlate, TrespassingLocation, Lawyer
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json


logger = logging.getLogger(__name__)



def get_all_deals(request):
    try:
        if request.method == 'GET':
            deals = Deal.objects.all()
            deal_list = []
            for deal in deals:
                deal_info = {
                    'deal_id': str(deal.deal_id),
                    'created_at': deal.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_at': deal.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'license_plate_uuid_id': str(deal.license_plate_uuid_id),  # Assuming this is the UUID field
                    'trespassing_location_id': str(deal.trespassing_location_id),
                    'plate_number': deal.license_plate_uuid.plate_number,
                    'location': deal.trespassing_location.location_address,
                    'work_step': deal.workflow_step.name_of_step 
                }
                deal_list.append(deal_info)
            return deal_list
        else:
            return JsonResponse({"error": "Only GET requests are allowed."}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
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

@login_required(login_url="/login/")
def index(request):
    deals = get_all_deals(request)  
    print(deals)

    context = {'segment': 'index', 'deals': deals}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def deal_detail(request, deal_id):
    try:
        deal = Deal.objects.get(deal_id=deal_id)
        html_template = loader.get_template('home/map.html')

        lawyers = Lawyer.objects.all()
        workflow_steps = WorkflowStep.objects.all()
        authorities = Authorities.objects.all()

        context = {'deal': deal, 'lawyers': lawyers, 'workflow_steps': workflow_steps, 'authorities': authorities}
        
        # Printing all lawyers
        for lawyer in lawyers:
            print(lawyer)

        return HttpResponse(html_template.render(context, request))
    except Deal.DoesNotExist:
        return HttpResponse("Deal not found", status=404)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
@csrf_exempt
def create_deal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trespassing_info = extract_trespassing_info(data)
            for info in trespassing_info:
                license_plate_number = info['license_plate']
                datetime_of_trespassing = info['datetime_of_trespassing']
                image_url = info.get('image_url', '')
                location_address = info['location']

                existing_license_plate = LicencePlate.objects.filter(plate_number=license_plate_number).first()
                existing_location = TrespassingLocation.objects.filter(location_address=location_address).first()
                
                if existing_license_plate:
                    license_plate_instance = existing_license_plate
                else:
                    # Create a new LicencePlate instance
                    license_plate_instance = LicencePlate.objects.create(plate_number=license_plate_number)

                if existing_location:
                    location_instance = existing_location
                else:
                    # Create a new TrespassingLocation instance
                    location_instance = TrespassingLocation.objects.create(location_address=location_address)

                lawyer_id = info.get('lawyer_id', '')

                # Create or get the Deal instance
                deal, created = Deal.objects.get_or_create(
                    license_plate_uuid=license_plate_instance,
                    trespassing_location=location_instance,
                    defaults={'created_at': datetime_of_trespassing, 'lawyer_id': lawyer_id}  
                )

                # Update the Deal instance if it already exists
                if not created:
                    deal.created_at = datetime_of_trespassing
                    deal.image_url = image_url
                    deal.lawyer_id = '' if deal.lawyer_id is None else deal.lawyer_id
                    deal.save()

            return JsonResponse({"message": "Deals created successfully.", "trespassing_info": trespassing_info})
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON data.", "details": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

def update_deal(request):
    if request.method == 'POST':
        deal_id = request.POST.get('deal_id')
  
        lawyer_name = request.POST.get('lawyer')
        work_step = request.POST.get('work_step')


        deal = get_object_or_404(Deal, deal_id=deal_id)

        lawyer, _ = Lawyer.objects.get_or_create(lawyer_name=lawyer_name)
        work_step , _= WorkflowStep.objects.get_or_create(name_of_step=work_step)

        deal.lawyer = lawyer
        deal.workflow_step = work_step
        deal.save()

        return HttpResponse("Form data received successfully!")
    else:
        return HttpResponse("Invalid request method")
