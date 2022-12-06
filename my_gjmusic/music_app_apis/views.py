from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Destination, Person
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from music_app_apis.serializers import PersonSerializer
# Create your views here.


@csrf_exempt
def person_details(request):
    if request.method == 'GET':
        dests = list(Person.objects.values())

        return JsonResponse(
                {"status:": "Success", "message": dests},
                status=200)

    elif request.method == 'POST':
        person_data = JSONParser().parse(request)
        person_serializer = PersonSerializer(data= person_data)
        if person_serializer.is_valid():
            person_serializer.save()
            return JsonResponse({"status:": "Success", "message": (list(Person.objects.values()))}, status = 200)

    elif request.method == 'PUT':
        person_data = JSONParser().parse(request)
        get_parsed_current_data = Person.objects.get(id = person_data['id'])
        person_serializer = PersonSerializer(get_parsed_current_data, data= person_data)
        if person_serializer.is_valid():
            person_serializer.save()
            return JsonResponse({"status:": "Updated Successfully"}, status = 204)
        return JsonResponse({"status:": "Failed to Update"}, status = 424)
    
    elif request.method == 'DELETE':
        person_data = JSONParser().parse(request)
        get_person_data = Person.objects.get(id = person_data['id'])

        return JsonResponse({"status:": "Deleted Succesfully", "message": get_person_data}, status = 202)