from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import io
from PIL import Image as PilImage  

from django.conf import settings
from eco_vision_api_bank_app.models import WasteBank, WasteType

MODEL_PATH = os.path.join(settings.BASE_DIR, 'best_model.h5')
model = load_model(MODEL_PATH)

IMG_SIZE = (224, 224)

index_to_class = {
    0: 'battery',
    1: 'biological',
    2: 'cardboard',
    3: 'clothes',
    4: 'glass',
    5: 'metal',
    6: 'paper',
    7: 'plastic',
    8: 'shoes',
    9: 'trash'
}

class PredictImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response({'error': 'File gambar tidak ditemukan'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['image']

        try:
            img = PilImage.open(io.BytesIO(file.read())).convert('RGB')
            img = img.resize(IMG_SIZE)
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            predictions = model.predict(img_array)
            predicted_index = int(np.argmax(predictions))
            predicted_class = index_to_class.get(predicted_index, 'Unknown')

            try:
                waste_type = WasteType.objects.get(name__iexact=predicted_class)
                banks = WasteBank.objects.filter(waste_processed=waste_type).prefetch_related('opening_hours')

                banks_data = []
                for bank in banks:
                    opening_hours = [
                        {
                            "day": oh.day,
                            "open_time": oh.open_time.strftime('%H:%M'),
                            "close_time": oh.close_time.strftime('%H:%M')
                        } for oh in bank.opening_hours.all()
                    ]
                    banks_data.append({
                        "name": bank.name,
                        "latitude": bank.latitude,
                        "longitude": bank.longitude,
                        "opening_hours": opening_hours
                    })
            except WasteType.DoesNotExist:
                banks_data = []

            return Response({
                "predicted_class": predicted_class,
                "class_index": predicted_index,
                "info": {
                    "description": f"Jenis sampah ini dikenali sebagai '{predicted_class}'.",
                    "how_to_process": "Sampah ini bisa dipisahkan dan dibawa ke bank sampah yang sesuai."
                },
                "recommended_banks": banks_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Gagal memproses gambar: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
