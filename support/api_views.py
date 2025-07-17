from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FAQListAPIView(APIView):
    def get(self, request):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED)

class ContactAPIView(APIView):
    def post(self, request):
        return Response({"message": "API en cours de développement"}, status=status.HTTP_501_NOT_IMPLEMENTED) 