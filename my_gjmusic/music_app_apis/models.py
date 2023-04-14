from django.db import models

# Create your models here.

# By Vicky
# class Person(models.Model):
#first_name = models.CharField(max_length=30)
#last_name = models.CharField(max_length=30)

class UserInfo(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    phone_number = models.BigIntegerField()
    name = models.CharField(max_length=255)

class AllSongs(models.Model):
    song_name = models.CharField(max_length=255)
    song_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=255)
    artists = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    overall_song_rating = models.FloatField()

class SongRating(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    song_id = models.ForeignKey(AllSongs, on_delete=models.CASCADE)
    song_rating = models.IntegerField()

class Playlist(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    song_id = models.ForeignKey(AllSongs, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

class Recommendation(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    recommended_user_id =  models.CharField(max_length=255)
    song_id = models.ForeignKey(AllSongs, on_delete=models.CASCADE)
    genre = models.CharField(max_length=255, null=True, blank=True)
    artists = models.CharField(max_length=255, null=True, blank=True)
    album = models.CharField(max_length=255, null=True, blank=True)