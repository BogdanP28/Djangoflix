from django.utils import timezone #type: ignore
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions

def publish_state_pre_save(sender, instance, *args, **kwargs):
    # Signal for the receiver function
    is_publish = instance.state == PublishStateOptions.PUBLISH
    is_draft = instance.state == PublishStateOptions.DRAFT
    if is_publish  and instance.publish_timestamp is None:
        # If the state is changed to published and we don't already have a timestamp we create on
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None

def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)