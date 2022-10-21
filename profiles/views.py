from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

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

    def get(self, request):
        profiles = User.objects.all()
        serializer = serializers.ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDetail(APIView):

    def get(self, request, pk):
        try:
            profile = User.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                "Profile doesnot exist.", status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data)
