from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from profiles import serializers
from profiles.models import create_auth_token, User # noqa


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = serializers.RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        token = Token.objects.get(user=user).key
        data = {
            "message": f"{user.username} Succesfully registerd !",
            "token": token
        }
        data.update(serializer.data)
        return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        data = f"{request.user.username} logoout Successful !"
        return Response(data=data, status=status.HTTP_200_OK)


class ProfileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = User.objects.all()
        serializer = serializers.ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "Profile doesnot exist.", status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data)


class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action, pk):
        try:
            target_user = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "target Profile doesnot exist.",
                status=status.HTTP_400_BAD_REQUEST
            )

        current_user = request.user
        target_user_followers = target_user.followers
        if action == "follow":
            if current_user in target_user_followers.all():
                return Response(
                    f"You are already following {target_user.username}.",
                    status=status.HTTP_400_BAD_REQUEST
                )

            else:
                target_user_followers.add(current_user.id)

            return Response(
                f"successfully following {target_user.username}.",
                status=status.HTTP_200_OK
            )

        elif action == "unfollow":
            if current_user not in target_user_followers.all():
                return Response(
                    f"you are not following {target_user.username}.",
                    status=status.HTTP_400_BAD_REQUEST
                )

            else:
                target_user_followers.remove(current_user)
                return Response(
                    f"successfully unfollowed {target_user.username}."
                )

        else:
            return Response(
                "Invalid action", status=status.HTTP_400_BAD_REQUEST
            )
