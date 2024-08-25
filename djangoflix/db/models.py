from django.db import models

# Create your models here.
class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAY_VA
    PUBLISH = "PU", "Publish"
    DRAFT = "DR", "Draft"
    # UNLISTED = "UN", "Unlisted"
    # PRIVATE = "PR", "Private"
    