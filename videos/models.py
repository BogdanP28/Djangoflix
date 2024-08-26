from django.db import models
from django.utils import timezone #type: ignore
from django.utils.text import slugify
from django.db.models.signals import pre_save
from djangoflix.db.models import PublishStateOptions
from djangoflix.db.receivers import publish_state_pre_save, slugify_pre_save
# Create your models here.
# class PublishStateOptions(models.TextChoices):
#     # CONSTANT = DB_VALUE, USER_DISPLAY_VA
#     PUBLISH = "PU", "Publish"
#     DRAFT = "DR", "Draft"
#     # UNLISTED = "UN", "Unlisted"
#     # PRIVATE = "PR", "Private"

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte = now
        )

class VideoManager(models.Manager):
    def get_queryset(self):
        # self.model is the actual model itself -> Video
        # self._db is the current db
        return VideoQuerySet(self.model, using=self._db) 
    
    def published(self):
        return self.get_queryset().published()
    
class Video(models.Model):
    # VideoStateOptions = PublishStateOptions
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) # 'this-is-my-video'
    video_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True) # when it was added in the db
    updated = models.DateTimeField(auto_now=True) # when it was saved
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    
    objects = VideoManager() # default model manager
    
    @property
    def is_published(self):
        return self.active
    
    def get_playlist_ids(self):
        return list(self.playlist_featured.all().values_list('id', flat=True)) #type: ignore
    
    # def save(self, *args, **kwargs):
    #     # Overwrite original safe
    #     if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
    #         # If the state is changed to published and we don't already have a timestamp we create on
    #         self.publish_timestamp = timezone.now()
    #     elif self.state == self.VideoStateOptions.DRAFT:
    #         self.publish_timestamp = None
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)
    
class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video "
        verbose_name_plural = "Published Videos"
        
class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video "
        verbose_name_plural = "All Videos"
        
# def publish_state_pre_save(sender, instance, *args, **kwargs):
#     # Signal for the receiver function
#     is_publish = instance.state == PublishStateOptions.PUBLISH
#     is_draft = instance.state == PublishStateOptions.DRAFT
#     if is_publish  and instance.publish_timestamp is None:
#         # If the state is changed to published and we don't already have a timestamp we create on
#         instance.publish_timestamp = timezone.now()
#     elif is_draft:
#         instance.publish_timestamp = None
    

# def slugify_pre_save(sender, instance, *args, **kwargs):
#     title = instance.title
#     slug = instance.slug
#     if slug is None:
#         instance.slug = slugify(title)
        
pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)