from rest_framework import serializers
from movies.models import Movie, Rating_options


class MovieSerializer(serializers.Serializer):
    added_by = serializers.SerializerMethodField()
    duration = serializers.CharField(allow_null=True, default=None)
    id = serializers.IntegerField(read_only=True)
    rating = serializers.ChoiceField(
        choices=Rating_options.choices, default=Rating_options.G
    )
    synopsis = serializers.CharField(allow_null=True, default=None)
    title = serializers.CharField(max_length=127)

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)

    def get_added_by(self, obj: Movie):
        return obj.user.email
