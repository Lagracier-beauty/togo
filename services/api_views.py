from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ServiceListAPIView(APIView):
    def get(self, request):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ServiceDetailAPIView(APIView):
    def get(self, request, pk):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED) 