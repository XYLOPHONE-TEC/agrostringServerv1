from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AgroStringsTVSchedule

# In a real-world scenario, you would want to secure this webhook,
# for example, by checking a secret key passed in the headers
# or by whitelisting the IP address of the media server.

class StreamOnPublishView(APIView):
    """
    Webhook called by the RTMP server when a stream starts.
    """
    def post(self, request, *args, **kwargs):
        stream_key = request.data.get("name")
        if not stream_key:
            return Response(
                {"detail": "Stream key not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule = get_object_or_404(AgroStringsTVSchedule, stream_key=stream_key)
        schedule.is_live = True
        schedule.save()

        return Response(
            {"detail": f"Stream {stream_key} is now live."}, status=status.HTTP_200_OK
        )


class StreamOnPublishDoneView(APIView):
    """
    Webhook called by the RTMP server when a stream ends.
    """
    def post(self, request, *args, **kwargs):
        stream_key = request.data.get("name")
        if not stream_key:
            return Response(
                {"detail": "Stream key not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule = get_object_or_404(AgroStringsTVSchedule, stream_key=stream_key)
        schedule.is_live = False
        schedule.save()

        return Response(
            {"detail": f"Stream {stream_key} has ended."}, status=status.HTTP_200_OK
        )