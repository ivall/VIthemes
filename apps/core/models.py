import uuid as uuid
from django.db import models

from config import OFFICIAL_THEMES


class Theme(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=16)
    image = models.URLField()
    primary_color = models.CharField(max_length=7)
    css = models.TextField()
    supported_theme = models.CharField(max_length=16, choices=OFFICIAL_THEMES)
    description = models.CharField(max_length=2048)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def count_votes(self):
        """
        Returns 3 elements, upvotes, downvotes, summary of votes
        """
        votes = Vote.objects.filter(theme=self)
        upvotes = votes.filter(choice='upvote')
        downvotes = votes.filter(choice='downvote')

        points = upvotes.count() - downvotes.count()
        return [upvotes, downvotes, points]


class VoteChoice(models.TextChoices):
    UPVOTE = "upvote", "upvote"
    DOWNVOTE = "downvote", "downvote"


class Vote(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    choice = models.CharField(choices=VoteChoice.choices, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)