from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="get_followed_profiles")

    def serialize(self,user):
        return {
            "profile_id": self.user.id,
            "profile_username": self.user.username,
            "followers": self.followers.count(),
            "following": self.user.get_followed_profiles.count(),
            "currently_following": not user.is_anonymous and self in user.get_followed_profiles.all(),
            "follow_available": (not user.is_anonymous) and self.user != user
            
        }
    
    def __str__(self):
        followers_str = ""
        for follower in self.followers.all():
            followers_str+= " " + follower.username
        return f"{self.user.username} (id {self.user.id}) - followed by {followers_str}"

class Post(models.Model):
    content = models.CharField(max_length=280)
    created_date = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="get_all_posts")
    likes = models.ManyToManyField(Profile, blank=True, related_name="get_all_liked_posts")

    def serialize(self, user):
        return {
            "id": self.id,
            "content": self.content,
            "created_date": self.created_date.strftime("%b %#d %Y, %#I:%M %p"),
            "creator_id": self.creator.id,
            "creator_username": self.creator.user.username,
            "likes": self.likes.count(),
            "liked": not user.is_anonymous and self in Profile.objects.filter(user=user).first().get_all_liked_posts.all(),
            "editable": self.creator.user == user
        }
