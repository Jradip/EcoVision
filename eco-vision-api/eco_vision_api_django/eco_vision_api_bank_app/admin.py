from django.contrib import admin
from .models import WasteBank, WasteType, OpeningHour


class OpeningHourInline(admin.TabularInline):
    model = OpeningHour
    extra = 0
    can_delete = False
    show_change_link = False
    readonly_fields = ['id']
    fields = ['id', 'day', 'open_time', 'close_time']
    max_num = 7  

@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank', 'day', 'open_time', 'close_time']
    list_filter = ['day', 'bank']
    search_fields = ['bank__name', 'day']
    readonly_fields = ['id']

@admin.register(WasteBank)
class WasteBankAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'latitude', 'longitude', 'get_waste_types']
    search_fields = ['name']
    readonly_fields = ['id']
    inlines = [OpeningHourInline]

    def get_waste_types(self, obj):
        return ", ".join([wt.name for wt in obj.waste_processed.all()])
    get_waste_types.short_description = 'Waste Types'


@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    readonly_fields = ['id']
