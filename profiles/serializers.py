from profiles import models

from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    password_2 = serializers.CharField(
        style={'input_type': 'password'}, required=True, write_only=True
    )

    class Meta:
        model = models.User
        fields = ['username', 'email', 'bio', 'password', 'password_2']

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']
        if self.validated_data['password_2'] != password:
            raise serializers.ValidationError("Password didn't match")

        user = models.User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError(
                "User with the given email already exists"
            )

        account = models.User(
            email=email, username=self.validated_data['username']
        )
        account.set_password(password)
        account.save()
        return account


class EachProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'bio', 'followers', 'following')
        read_only_fields = (
            'id', 'username', 'email', 'bio', 'followers', 'following'
        )


class ProfileSerializer(serializers.ModelSerializer):
    following = EachProfileSerializer(many=True, read_only=True)
    followers = EachProfileSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'bio', 'followers', 'following')
