from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from .models import UserInfo, AllSongs, SongRating, Playlist, Recommendation
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from music_app_apis.serializers import UserInfoSerializer, AllSongsSerializer, RecommendationSerializer, PlaylistSerializer, SongRatingSerializer

import uuid
import json

# Create your views here.

@csrf_exempt
def upload_songs(request):
    if request.method == 'PUT':
        song_info = json.loads(request.body)

        mandatory_fields = ['song_name', 'artist_name', 'album_name', 'genre_name']
        for i in mandatory_fields:
            if not i in song_info:
                return JsonResponse({"message": f"{i} is a mandatory_field"}, status=400)
        
        exsists_ = AllSongs.objects.filter(song_name=song_info['song_name']).values('song_id')

        if exsists_:
            return JsonResponse({"message": "This Song already exsists in the table"}, status=400)

        song_info['song_id'] = uuid.uuid4()
        song_info['overall_song_rating'] = song_initial_rating = 0.0

        
        AllSongs.objects.create(song_name = song_info['song_name'], genre = song_info['genre_name'], artists = song_info['artist_name'], album = song_info['album_name'], song_id = song_info['song_id'], overall_song_rating= song_initial_rating)

        return JsonResponse({"Message": "song information uploaded in the song table"}, status=200)


def get_all_songs(request):
    if request.method == 'GET':
        params = request.GET.dict()
        if params:
            all_songs = AllSongs.objects.filter(**params)
        else:
            all_songs = AllSongs.objects.all()
        serializer = AllSongsSerializer(all_songs, many=True)
        return JsonResponse({"message": serializer.data}, status=200)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        login_info = json.loads(request.body)

        mandatory_fields = ['name', 'phone_number', 'user_id']

        for i in mandatory_fields:
            if not i in login_info:
                return JsonResponse({"message": f"{i} is a mandatory_field"}, status=400)
            
        exsists_ = UserInfo.objects.filter(Q(user_id=login_info['user_id']) | Q(phone_number=login_info['phone_number'])).values('name')

        if exsists_:
            return JsonResponse({"message": "This username or phonenumber already exsists in the table"}, status=400)
        
        serializer = UserInfoSerializer(data=login_info)
        if serializer.is_valid():
            serializer.save()

        return JsonResponse({"Message": "Login successfully created"}, status=200)
            
        


# @csrf_exempt
# def person_details(request):
#     if request.method == 'GET':
#         dests = list(Person.objects.values())

#         return JsonResponse(
#                 {"status:": "Success", "message": dests},
#                 status=200)

#     elif request.method == 'POST':
#         person_data = JSONParser().parse(request)
#         person_serializer = PersonSerializer(data= person_data)
#         if person_serializer.is_valid():
#             person_serializer.save()
#             return JsonResponse({"status:": "Success", "message": (list(Person.objects.values()))}, status = 200)

#     elif request.method == 'PUT':
#         person_data = JSONParser().parse(request)
#         get_parsed_current_data = Person.objects.get(id = person_data['id'])
#         person_serializer = PersonSerializer(get_parsed_current_data, data= person_data)
#         if person_serializer.is_valid():
#             person_serializer.save()
#             return JsonResponse({"status:": "Updated Successfully"}, status = 204)
#         return JsonResponse({"status:": "Failed to Update"}, status = 424)
    
#     elif request.method == 'DELETE':
#         person_data = JSONParser().parse(request)
#         get_person_data = Person.objects.get(id = person_data['id'])

#         return JsonResponse({"status:": "Deleted Succesfully", "message": get_person_data}, status = 202)