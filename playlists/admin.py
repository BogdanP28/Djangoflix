from re import T
from typing import Any
from django.contrib import admin
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.http import HttpRequest

from playlists.models import PlaylistQuerySet

# Register your models here.
from .models import MovieProxy, Playlist, PlaylistItem, TVShowProxy, TVShowSeasonProxy
# ------------------------ MovieProxy ------------------------
class MovieProxyAdmin(admin.ModelAdmin):
    list_display: list[str] = ['title']
    fields: list[str] = ["title", "description", "slug", "state", "video"] 
    
    class Meta:
        model = MovieProxy
        
    def get_queryset(self, request) -> BaseManager[MovieProxy]:
        return MovieProxy.objects.all()
    
admin.site.register(MovieProxy, MovieProxyAdmin)

# ------------------------ TV Show Season --------------------
class SeasonEpisodeInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0
    
class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inline: list[type[SeasonEpisodeInline]] = [SeasonEpisodeInline]
    list_display: list[str] = ["title", "parent"]
    
    class Meta:
        model = TVShowSeasonProxy
    
    def get_queryset(self, request) -> PlaylistQuerySet:
        return TVShowSeasonProxy.objects.all()
        
admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)

# ------------------------ TV Show --------------------
class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields: list[str] = ["order", "title", "state"]

class TVShowProxyAdmin(admin.ModelAdmin):
    list_display: list[str] = ['title']
    fields: list[str] = ["title", "description", "slug", "state", "video"] 
    inlines: list[type[TVShowSeasonProxyInline]] = [TVShowSeasonProxyInline]
    
    class Meta:
        model = TVShowProxy
    
    def get_queryset(self, request) -> PlaylistQuerySet:
        return TVShowProxy.objects.all()
         
admin.site.register(TVShowProxy, TVShowProxyAdmin)

# ------------------------ Playlist --------------------
class PlaylistItemInLine(admin.TabularInline):
    model: type[PlaylistItem] = PlaylistItem
    extra: int = 0

class PlaylistAdmin(admin.ModelAdmin):
    inlines: list[type[PlaylistItemInLine]] = [PlaylistItemInLine]
    
    class Meta:
        model = Playlist
        
    def get_queryset(self, request) -> BaseManager[Playlist]:
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)

admin.site.register(Playlist, PlaylistAdmin)