from django.db import models
import uuid

class WasteType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class WasteBank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    waste_processed = models.ManyToManyField(WasteType)

    def __str__(self):
        return self.name


class OpeningHour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    DAY_CHOICES = [
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
        ('minggu', 'Minggu'),
    ]
    bank = models.ForeignKey(WasteBank, on_delete=models.CASCADE, related_name='opening_hours')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        unique_together = ('bank', 'day')

    def __str__(self):
        return f"{self.bank.name} - {self.day}"

class TrashCan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    accepted_waste_types = models.ManyToManyField(WasteType)

    def __str__(self):
        return f"Trash Can at ({self.latitude}, {self.longitude})"
