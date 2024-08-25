from django.test import TestCase
from .models import Video, PublishStateOptions
from django.utils import timezone #type: ignore
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions

# Create your tests here.
class VideoModelTestCase(TestCase):
    def setUp(self):
        self.obj_a = Video.objects.create(title="Test Title", video_id='abc')
        self.obj_b = Video.objects.create(title="This is my title", state=PublishStateOptions.PUBLISH, video_id='def')
    
    def test_slug_field(self):
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.obj_a.slug)
    
    def test_valid_title(self):
        title = "Test Title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
    def test_created_count(self):
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 2)
        
    def test_draft_case(self):
        qs = Video.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)
        
    def test_publish_case(self):
        qs = Video.objects.filter(state=PublishStateOptions.PUBLISH)
        self.assertEqual(qs.count(), 1)
        now = timezone.now()
        publish_qs = Video.objects.filter(
                                            state=PublishStateOptions.PUBLISH,
                                            publish_timestamp__lte=now)
        self.assertTrue(publish_qs.exists())
        
    def test_publish_manager(self):
        published_qs = Video.objects.all().published() #type: ignore
        published_qs_2 = Video.objects.published() #type: ignore
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs_2.count())