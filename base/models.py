from django.db import models

# Create your models here.


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=(("M", "Male"), ("F", "Female")))
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Match(models.Model):
    datetime = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=(
            ("upcoming", "upcoming"),
            ("ongoing", "ongoing"),
            ("completed", "completed"),
            ("cancelled", "cancelled"),
        ),
    )
    first_player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="first_player"
    )
    second_player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="second_player"
    )
    first_player_points = models.IntegerField(default=0)
    second_player_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_player.__str__() + " vs " + self.second_player.__str__()
