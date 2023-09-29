from .models import Player, Match
from django.contrib import admin


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "gender",
        "dob",
        "created_at",
        "updated_at",
    ]
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "datetime",
        "status",
        "first_player",
        "second_player",
        "first_player_points",
        "second_player_points",
        "created_at",
        "updated_at",
    ]
    pass
