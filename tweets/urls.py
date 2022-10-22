from django.urls import path
from .views import TweetView, FeedView, TweetDetailView


# router = SimpleRouter()
# router.register('tweet', TweetView)
# urlpatterns = router.urls


urlpatterns = [
    path('', TweetView.as_view(), name='tweet-list'),
    path('<int:pk>', TweetDetailView.as_view(), name='detail'),
    path("feed/", FeedView.as_view(), name="feed")
]
