from rest_framework import serializers
from base.models import Player, Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"