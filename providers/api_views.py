from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProviderRegisterAPIView(APIView):
    def post(self, request):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ProviderProfileAPIView(APIView):
    def get(self, request):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ProviderOrdersAPIView(APIView):
    def get(self, request):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ProvidersListAPIView(APIView):
    def get(self, request):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED) 