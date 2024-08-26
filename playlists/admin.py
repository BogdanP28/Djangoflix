from django.contrib import admin

# Register your models here.
from .models import Playlist, PlaylistItem


class PlaylistItemInLine(admin.TabularInline):
    model = PlaylistItem
    extra = 0

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistItemInLine]
    class Meta:
        model = Playlist

admin.site.register(Playlist, PlaylistAdmin)