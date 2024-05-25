from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Hello

# Create your views here.

class Db(APIView):
    def get(self, request):
        data = Hello.objects.all()
        return Response({"message": data})