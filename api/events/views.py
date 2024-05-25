from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from .models import Event
from .serializers import EventSerializer

# Create your views here.

class EventView(APIView):

    # 商品操作に関する関数で共通で使用する商品取得関数
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound

    """
    イベント操作に関する関数
    """
    def get(self, request, id=None, format=None):
        """
        イベントを取得する
        """
        if id is None :
            queryset = Event.objects.all()
            serializer = EventSerializer(queryset, many=True)
        else: 
            event_instance = self.get_object(id)
            serializer = EventSerializer(event_instance)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """
        商品を登録する
        """
        serializer = EventSerializer(data=request.data)
        # validationを通らなかった場合、例外を投げる
        serializer.is_valid(raise_exception=True)
        # 検証したデータを永続化する
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)