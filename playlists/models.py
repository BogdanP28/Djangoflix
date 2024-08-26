from django.db import models
from django.utils import timezone #type: ignore
from django.utils.text import slugify
from django.db.models.signals import pre_save
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save
from videos.models import Video
# Create your models here.
class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte = now
        )

class PlaylistManager(models.Manager):
    def get_queryset(self):
        # self.model is the actual model itself -> Video
        # self._db is the current db
        return PlaylistQuerySet(self.model, using=self._db) 
    
    def published(self):
        return self.get_queryset().published()
    
class Playlist(models.Model):
    # VideoStateOptions = PublishStateOptions
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # 'this-is-my-video' 
    video = models.ForeignKey(Video, blank=True, related_name ="playlist_featured", null=True, on_delete=models.SET_NULL) # one video per playlist
    videos = models.ManyToManyField(Video, blank=True, related_name='playlist_item', through="PlaylistItem")
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True) # when it was added in the db
    updated = models.DateTimeField(auto_now=True) # when it was saved
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    
    objects = PlaylistManager() # default model manager
    
    @property
    def is_published(self):
        return self.active
    
        
pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)

class PlaylistItem(models.Model):
    # playlist_obj.playlistitem_set.all()
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-timestamp']
    
    #qs = PlaylistItem.objects.filter(playlist=playlist_obj).order_by("order")