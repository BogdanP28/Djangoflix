from django.contrib import admin
from django.db.models.manager import BaseManager

# Register your models here.
from .models import Video, VideoAllProxy, VideoPublishedProxy

class VideoAllAdmin(admin.ModelAdmin):
    list_display: list[str] = ["title", "id", "state", "video_id", "is_published", "get_playlist_ids"]
    search_fields: list[str] = ["title"]
    list_filter: list[str] = ["active", "state"]
    readonly_fields: list[str] = ["id", "is_published", "publish_timestamp", "get_playlist_ids"]
    
    class Meta:
        model = VideoAllProxy
    
    # def published(self, obj, *args, **kwargs):
    #     return obj.active
        
        
class VideoPublishProxyAdmin(admin.ModelAdmin):
    list_display: list[str] = ["title", "video_id"]
    search_fields: list[str] = ["title"]
    # list_filter = ["video_id"]
    class Meta:
        model = Video
    
    def get_queryset(self, request) -> BaseManager[VideoPublishedProxy]:
        return VideoPublishedProxy.objects.filter(active=True)

admin.site.register(VideoAllProxy, VideoAllAdmin)

admin.site.register(VideoPublishedProxy, VideoPublishProxyAdmin)