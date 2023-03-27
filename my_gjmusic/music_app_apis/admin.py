from django.contrib import admin
from .models import UserInfo, AllSongs, SongRating, Playlist, Recommendation

# Register your models here.

admin.site.register(UserInfo)
admin.site.register(AllSongs)
admin.site.register(SongRating)
admin.site.register(Playlist)
admin.site.register(Recommendation)