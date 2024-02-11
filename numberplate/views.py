from django.http import JsonResponse
from .models import TrespassingEvent, Deal, Thread , ThreadImage , AccessToken
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


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

                license_plate, created = LicensePlate.objects.get_or_create(plate_number=license_plate_number)
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