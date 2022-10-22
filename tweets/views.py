from django.db.models import Q

from rest_framework.views import APIView
from .models import Tweet
from .serializers import TweetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TweetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Tweet.objects.filter(
            tweeter=request.user
        ).order_by('-created_at')

        if not data.exists():
            return Response("You have not posted any tweets.")

        serializer = TweetSerializer(data, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        context = {"user": request.user}
        serializer = TweetSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        return Response(serializer.data, status=200)


class TweetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            tweet = Tweet.objects.get(id=pk)
        except Tweet.DoesNotExist:
            return Response("tweet does not exist.", status=404)

        if request.user not in tweet.tweeter.followers.all() and tweet.tweeter != request.user: # noqa
            return Response(
                "you are not permitted to access this tweet", status=403
            )

        serializer = TweetSerializer(tweet)
        return Response(serializer.data, status=200)


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Tweet.objects.filter(
            Q(tweeter__in=request.user.following.all()) |
            Q(tweeter=request.user)
        ).order_by("-created_at")

        serializer = TweetSerializer(data, many=True)
        return Response(serializer.data)
