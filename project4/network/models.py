from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="following")

    def __str__(self):
        return str(self.user)

    def serialize(self, other):
        is_following = other.is_authenticated and self in other.following.all()
        can_follow = other.is_authenticated and self.user != other

        return {
            "id": self.id,
            "username": self.user.username,
            "numFollowers": self.followers.count(),
            "numFollowing": self.user.following.count(),
            "isFollowing": is_following,
            "canFollow": can_follow
        }


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_posts")
    text = models.CharField(max_length=256)
    likes = models.ManyToManyField(User, blank=True, related_name="get_likes")
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Post #{self.id} by {self.user}"

    def serialize(self, other):
        liked = other.is_authenticated and self in other.get_likes.all()
        can_edit = other.is_authenticated and self.user == other
        
        return {
            "id": self.id,
            "user": self.user.username,
            "userID": self.user.id,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "numLikes": self.likes.count(),
            "liked": liked,
            "canEdit": can_edit
        }
