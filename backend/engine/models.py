from django.db import models
import uuid
import unidecode

class Tag(models.Model):
    """
    A tag is the way to link images together. It's only a word that can represent
    people, dates or facts.
    Be careful in the way for spelling tags to avoid having 'Chambery', 'chambéry', 'chy', 'Chy'...
    """
    tag = models.CharField(max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag


class Picture(models.Model):
    """
    A picture is an id (= used to compute the path to the thumbnail and the full image)
    and a list of tags (for context)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    hash = models.CharField(max_length=80, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Neighbors(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    from_picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='from_picture')
    to_picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='to_picture')
    distance = models.FloatField(default=0)

    def __str__(self):
        return 'Neigbors of {}'.format(self.from_picture_id)
