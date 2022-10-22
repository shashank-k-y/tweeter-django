from rest_framework import serializers

from commons.awsclient import get_presignedurl
from tweets.models import Tweet


CONTENT_TYPE_MAPPING = {
    "pdf": "application/pdf",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
}


class TweetSerializer(serializers.ModelSerializer):
    presigned_url = serializers.SerializerMethodField(
        method_name="get_presigned_url"
    )
    file = serializers.FileField(required=False)

    class Meta:
        model = Tweet
        fields = ('id', 'tweeter', 'file', 'text', "presigned_url")
        read_only_fields = ("tweeter",)
        required_fields = ('text')

    def get_presigned_url(self, instance):
        extention = instance.s3_key.split('.')[-1]
        if extention in CONTENT_TYPE_MAPPING:
            return get_presignedurl(
                key=instance.s3_key,
                content_type=CONTENT_TYPE_MAPPING[extention]
            )
        else:
            return None

    def create(self, validated_data):
        if validated_data.get('file'):
            file_name = validated_data['file'].name
            validated_data['s3_key'] = file_name
        validated_data['tweeter'] = self.context['user']
        return Tweet.objects.create(**validated_data)
