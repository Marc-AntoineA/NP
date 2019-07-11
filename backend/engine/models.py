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

    def __str__(self):
        return self.tag

    def __eq__(self, other):
        return unidecode.unidecode(self.lower()) == unidecode.unidecode(other.lower())


class Picture(models.Model):
    """
    A picture is an id (= used to compute the path to the thumbnail and the full image)
    and a list of tags (for context)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    hash = models.CharField(max_length=80, unique=True, editable=False)

    def __str__(self):
        return str(self.id)
