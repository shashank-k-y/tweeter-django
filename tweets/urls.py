from django.urls import path
from .views import TweetView, FeedList, TweetDetailView


urlpatterns = [
    path('', TweetView.as_view(), name='tweet-list'),
    path('<int:pk>', TweetDetailView.as_view(), name='detail'),
    path("feed/", FeedList.as_view(), name="feed")
]
