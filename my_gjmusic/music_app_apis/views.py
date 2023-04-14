import random
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

        mandatory_fields = ['song_name', 'artists', 'album', 'genre']
        for i in mandatory_fields:
            if not i in song_info:
                return JsonResponse({"message": f"{i} is a mandatory_field"}, status=400)
        
        exsists_ = AllSongs.objects.filter(song_name=song_info['song_name']).values('song_id')

        if exsists_:
            return JsonResponse({"message": "This Song already exsists in the table"}, status=400)
        song_info['overall_song_rating'] = 0.0

        serialized_data = AllSongsSerializer(data=song_info)
        if serialized_data.is_valid():
            try:
                AllSongsSerializer(serialized_data.save())
                return JsonResponse({"Message": "song information uploaded in the song table"}, status=200)
            except Exception as e:
                return JsonResponse({"message": f"Unable to upload in the song table - {e}"}, status=500)
        else:
            return JsonResponse({"message": f"Invalid request payload "}, status=400)


def get_all_songs(request):
    if request.method == 'GET':
        params = request.GET.dict()
        try:
            if params:
                all_songs = AllSongs.objects.filter(**params)
            else:
                all_songs = AllSongs.objects.all()
        except Exception as e:
                return JsonResponse({"message": f"{e}"}, status=500)

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
            
        

@csrf_exempt
def update_playlist(request):
    playlist_info = json.loads(request.body)

    if "user_id" not in playlist_info:
        return JsonResponse({"message": f"Login to create and share playlist", "sign_up": "http://127.0.0.1:8000/music/login"}, status=401)

    mandatory_fields = ['playlist_name', 'song_id']
    for i in mandatory_fields:
        if not i in playlist_info:
            return JsonResponse({"message": f"{i} is a mandatory_field"}, status=400)

    serialized_data = PlaylistSerializer(data=playlist_info)

    if serialized_data.is_valid():
        if request.method == 'PUT': #PUT Method
            if Playlist.objects.filter(user_id=playlist_info.get("user_id"), playlist_name=playlist_info.get("playlist_name"), song_id=playlist_info.get("song_id")).exists():
                return JsonResponse({"message": "This Song already added in this playlist"}, status=409)

            try:
                PlaylistSerializer(serialized_data.save())
                return JsonResponse({"Message": "Song added to playlist"}, status=200)
            except Exception as e:
                return JsonResponse({"message": f"Unable to add song in playlist {e}"}, status=500)
        elif request.method == 'DELETE': #DELETE Method
            try:
                if Playlist.objects.filter(user_id=playlist_info.get("user_id"), playlist_name=playlist_info.get("playlist_name"), song_id=playlist_info.get("song_id")).exists():
                        Playlist.objects.filter(user_id=playlist_info.get("user_id"), song_id=playlist_info.get("song_id"), playlist_name=playlist_info.get("playlist_name")).delete()
                        return JsonResponse({"message": "Song removed from playlist"}, status=204)
                return JsonResponse({"message": "Song doesn't exists playlist"}, status=204)
            except Exception as e:
                return JsonResponse({"message": f"Unable to delete the testset - {e}"}, status=500)
    else:
        list_ = ['song_id', 'user_id']
        if list(serialized_data.errors.keys())[0] in list_:
            return JsonResponse({"message": f"{list(serialized_data.errors.keys())[0]} does not exisits"}, status=400)

        return JsonResponse({"message": f"Invalid request payload"}, status=400)


        
@csrf_exempt
def recommend_song_to_friend(request):
    if request.method == 'POST':
        song_info = json.loads(request.body)

        mandatory_fields = ['song_id', 'genre', 'artists', 'album']

        common_keys = set(song_info.keys()).intersection(set(mandatory_fields))
        if not common_keys:
            return JsonResponse({"message": f"atleat any of these field is required, {mandatory_fields}"}, status=400)
        
        if Recommendation.objects.filter(**song_info).exists():
            return JsonResponse({"message": f"This song/ genre / artists / album is already been recommended to this user"}, status=409)
        
        if "recommended_user_id" not in song_info:
            return JsonResponse({"message": f"recommended_user_id is required"}, status=401)
        elif not UserInfo.objects.filter(user_id=song_info.get("recommended_user_id")).exists():
            return JsonResponse({"message": f"recommended_user_id does not exist"}, status=401)

        serialized_data = RecommendationSerializer(data=song_info)

        if serialized_data.is_valid():
            RecommendationSerializer(serialized_data.save())
            return JsonResponse({"message": f"song recommended successfully to user: {song_info.get('recommended_user_id')}"}, status=200)
        else:
            return JsonResponse({"message": serialized_data.errors})
        
    if request.method == 'GET':
        if request.body:
            song_info = json.loads(request.body)
            try:
                if song_info:
                    recommended_details = Recommendation.objects.filter(**song_info)
                else:
                    recommended_details = Recommendation.objects.all()
            except Exception as e:
                    return JsonResponse({"message": f"{e}"}, status=500)

            serializer = RecommendationSerializer(recommended_details, many=True)
            return JsonResponse({"message": serializer.data}, status=200)
        else:
            try:
                recommended_details = Recommendation.objects.all()
            except Exception as e:
                return JsonResponse({"message": f"{e}"}, status=500)

            serializer = RecommendationSerializer(recommended_details, many=True)
            return JsonResponse({"message": serializer.data}, status=200)
        




def suggest_by_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        
        if not query:
            return JsonResponse({"message": "Please provide a search query"}, status=400)

        songs = AllSongs.objects.filter(Q(song_name__icontains=query) | Q(genre__icontains=query) | Q(artists__icontains=query))

        results = [{
        'song_name': song.song_name,
        'genre': song.genre,
        'artists': song.artists
        } for song in songs]

        return JsonResponse({"results": results}, status=200)
    
@csrf_exempt
def recommended_for_you(request):
    if request.method == 'POST':
        user_id_ = json.loads(request.body)

        if not user_id_.get('user_id'):
            return JsonResponse({"message": "user_id is mandatory"}, status=400)

        song_ids = Playlist.objects.filter(user_id=user_id_.get('user_id')).values_list('song_id', flat=True)
        song_info_list = AllSongs.objects.filter(song_id__in=song_ids)

        list_genre = set()
        list_artists = set()
        list_album = set()

        for song_detail in song_info_list:
            list_genre.add(song_detail.genre)
            list_artists.add(song_detail.artists)
            list_album.add(song_detail.album)

        song_info_list = AllSongs.objects.filter(genre__in=list_genre, artists__in=list_artists, album__in=list_album).exclude(song_id__in=song_ids)
        serializer_song_info = AllSongsSerializer(song_info_list, many=True)

        num_request = user_id_['num_request'] if user_id_.get('num_request') else 16
        samples = random.sample(serializer_song_info.data, min(num_request, len(serializer_song_info.data)))

        return JsonResponse({"message": samples}, status=200)


@csrf_exempt
def give_song_rating(request):
    if request.method == 'PUT':
        song_rating_info = json.loads(request.body)

        mandatory_fields = ['user_id', 'song_id', 'song_rating']

        for i in mandatory_fields:
            if not i in song_rating_info:
                return JsonResponse({"message": f"{i} is a mandatory field"}, status=400)
            
        if song_rating_info['song_rating'] >5 or song_rating_info['song_rating'] < 1:
            return JsonResponse({"message": "song_rating should be give between 1 to 5"}, status = 400)

        try:
            user = UserInfo.objects.get(user_id=song_rating_info['user_id'])
        except UserInfo.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=400)

        try:
            id = AllSongs.objects.get(song_id=song_rating_info['song_id'])
        except AllSongs.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=400)
        
        SongRating.objects.update_or_create(
        user_id=user,
        song_id=id,
        defaults={"song_rating": song_rating_info['song_rating']}
        )
        return JsonResponse({"message": f"song rating given for the song_id:{song_rating_info['song_id']} is {song_rating_info['song_rating']}"}, status=200)

        


    


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