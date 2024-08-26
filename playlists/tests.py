from django.db.models.manager import BaseManager
from django.test import TestCase
from .models import Playlist, PublishStateOptions
from django.utils import timezone #type: ignore
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions
from videos.models import Video

# Create your tests here.
class PlaylistModelTestCase(TestCase):
    def create_videos(self):
        video_a: Video = Video.objects.create(title="Blade Runner original", video_id="abc123")
        video_b: Video = Video.objects.create(title="Blade Runner 2049", video_id="abc124")
        video_c: Video = Video.objects.create(title="Blade Runner 2099", video_id="abc125")
        self.video_a: Video = video_a
        self.video_b: Video = video_b
        self.video_c: Video = video_c
        self.video_qs: BaseManager[Video] = Video.objects.all()
        
    def setUp(self):
        self.create_videos()
        self.obj_a: Playlist = Playlist.objects.create(title="Test Title", video=self.video_a)
        obj_b: Playlist = Playlist.objects.create(title="This is my title", 
                                             state=PublishStateOptions.PUBLISH,
                                             video=self.video_a)
        
        # obj_b.videos.set([self.video_a, self.video_b, self.video_c])
        v_qs: BaseManager[Video] = self.video_qs
        obj_b.videos.set(v_qs)
        obj_b.save()
        self.obj_b: Playlist = obj_b
        
    def test_video_playlist(self):
        qs = self.video_a.playlist_featured.all() #type: ignore
        self.assertEqual(qs.count(),2)
        
    def test_playlist_video_items(self):
        count = self.obj_b.videos.all().count()
        self.assertEqual(count, 3)
        
    def test_playlist_video_through_model(self):
        video_qs = sorted(list(self.video_qs.values_list("id"))) # type: ignore
        playlist_obj_video_qs = sorted(list(self.obj_b.videos.all().values_list("id"))) #type: ignore
        playlist_obj_playlist_item_qs = sorted(list(self.obj_b.playlistitem_set.all().values_list("video"))) #type: ignore
        self.assertEqual(video_qs, playlist_obj_video_qs, playlist_obj_playlist_item_qs)
        
    def test_video_playlist_ids_propery(self):
        ids = self.obj_a.video.get_playlist_ids() #type: ignore
        actual_ids = list(Playlist.objects.filter(video=self.video_a).values_list("id", flat=True))
        self.assertEqual(ids, actual_ids)
    
    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)
    
    def test_valid_title(self):
        title = "This is my title"
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
    def test_created_count(self):
        qs = Playlist.objects.all()
        self.assertEqual(qs.count(), 2)
        
    def test_draft_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)
        
    def test_publish_case(self):
        qs = Playlist.objects.filter(state=PublishStateOptions.PUBLISH)
        self.assertEqual(qs.count(), 1)
        now = timezone.now()
        publish_qs = Playlist.objects.filter(
                                            state=PublishStateOptions.PUBLISH,
                                            publish_timestamp__lte=now)
        self.assertTrue(publish_qs.exists())
        
    def test_publish_manager(self):
        published_qs = Playlist.objects.all().published() #type: ignore
        published_qs_2 = Playlist.objects.published() #type: ignore
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())