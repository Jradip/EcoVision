from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import WasteBank
from .serializers import WasteBankSerializer

class WasteBankListView(ListAPIView):
    queryset = WasteBank.objects.all()
    serializer_class = WasteBankSerializer
    permission_classes = [IsAuthenticated]

from .models import TrashCan
from .serializers import TrashCanSerializer
from rest_framework.generics import ListAPIView

class TrashCanListView(ListAPIView):
    queryset = TrashCan.objects.all()
    serializer_class = TrashCanSerializer
    permission_classes = [IsAuthenticated]
