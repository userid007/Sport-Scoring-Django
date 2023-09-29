from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Player, Match
from .serializers import MatchSerializer, PlayerSerializer
from django.http import StreamingHttpResponse
import time
import json


def stream(request):
    def event_stream():
        while True:
            time.sleep(1)
            matches = Match.objects.all()
            data = MatchSerializer(matches, many=True).data
            for mach in data:
                first_player = Player.objects.get(id=mach["first_player"])
                second_player = Player.objects.get(id=mach["second_player"])
                mach["first_player"] = {
                    "first_name": first_player.first_name,
                    "last_name": first_player.last_name,
                }
                mach["second_player"] = {
                    "first_name": second_player.first_name,
                    "last_name": second_player.last_name,
                }
            yield "data: {}\n\n".format(json.dumps(data))

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


@api_view(["GET", "POST", "DELETE", "PUT"])
def player(request, pk=None):
    if request.method == "GET":
        # Get a single player
        if pk is not None:
            try:
                player = Player.objects.get(id=pk)
                serializer = PlayerSerializer(player, many=False)
                return Response(serializer.data)
            except Player.DoesNotExist:
                return Response({"msg": "Player does not exist"}, status=404)
        # Get all players
        else:
            player = Player.objects.all()
            serializer = PlayerSerializer(player, many=True)
            return Response(serializer.data)

    # Create a new player
    elif request.method == "POST" and pk is None:
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # Delete a player
    elif request.method == "DELETE" and pk is not None:
        try:
            player = Player.objects.get(id=pk)
            player.delete()
            return Response({"msg": "Successfully deleted a player"})
        except Player.DoesNotExist:
            return Response({"msg": "Player does not exist"}, status=404)

    # Update a player
    elif request.method == "PUT" and pk is not None:
        try:
            player = Player.objects.get(id=pk)
            serializer = PlayerSerializer(
                instance=player, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Player.DoesNotExist:
            return Response({"msg": "Player does not exist"}, status=404)

    else:
        return Response({"msg": "Method not allowed"}, status=405)


@api_view(["GET", "POST", "DELETE", "PUT"])
def match(request, pk=None):
    if request.method == "GET":
        # Get a single match
        if pk is not None:
            try:
                match = Match.objects.get(id=pk)
                data = MatchSerializer(match, many=False).data
                first_player = Player.objects.get(id=data["first_player"])
                second_player = Player.objects.get(id=data["second_player"])
                data["first_player"] = {
                    "first_name": first_player.first_name,
                    "last_name": first_player.last_name,
                }
                data["second_player"] = {
                    "first_name": second_player.first_name,
                    "last_name": second_player.last_name,
                }
                return Response(data)
            except Match.DoesNotExist:
                return Response({"msg": "Match does not exist"}, status=404)
        # Get all matches
        else:
            matches = Match.objects.all()
            data = MatchSerializer(matches, many=True).data
            for mach in data:
                first_player = Player.objects.get(id=mach["first_player"])
                second_player = Player.objects.get(id=mach["second_player"])
                mach["first_player"] = {
                    "first_name": first_player.first_name,
                    "last_name": first_player.last_name,
                }
                mach["second_player"] = {
                    "first_name": second_player.first_name,
                    "last_name": second_player.last_name,
                }
            return Response(data)

    # Create a new match
    elif request.method == "POST" and pk is None:
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            if (
                serializer.validated_data["first_player"]
                == serializer.validated_data["second_player"]
            ):
                return Response({"msg": "Players cannot be the same"}, status=400)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # Delete a match
    elif request.method == "DELETE" and pk is not None:
        try:
            match = Match.objects.get(id=pk)
            match.delete()
            return Response({"msg": "Successfully deleted match"})
        except Match.DoesNotExist:
            return Response({"msg": "Match does not exist"}, status=404)

    # Update a match
    elif request.method == "PUT" and pk is not None:
        match = Match.objects.get(id=pk)
        if (
            request.data.get("first_player_points") is not None
            or request.data.get("second_player_points") is not None
        ):
            if match.status != "ongoing":
                return Response({"msg": "Match is not ongoing"}, status=400)
            elif request.data.get("points") == "first":
                request.data["first_player_points"] += 1
            elif request.data.get("points") == "second":
                request.data["second_player_points"] += 1

        serializer = MatchSerializer(instance=match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            match = Match.objects.get(id=pk)
            if match.first_player_points == 30 or match.second_player_points == 30:
                match.status = "completed"
                match.save()
            elif (
                abs(match.first_player_points - match.second_player_points) >= 2
            ) and (match.first_player_points > 20 or match.second_player_points > 20):
                match.status = "completed"
                match.save()

            return Response(MatchSerializer(match, many=False).data)
        else:
            return Response(serializer.errors)
        # except Match.DoesNotExist:
        #     return Response({"msg": "Match does not exist"}, status=404)
    else:
        return Response({"msg": "Method not allowed"}, status=405)
