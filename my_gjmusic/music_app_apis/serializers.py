from rest_framework import serializers
from music_app_apis.models import UserInfo, AllSongs, Recommendation, Playlist, SongRating

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('__all__')

class AllSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllSongs
        fields = ('__all__')

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('__all__')

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('__all__')

class SongRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongRating
        fields = ('__all__')