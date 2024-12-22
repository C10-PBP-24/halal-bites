from django.contrib import admin
from .models import Tracker  # Import model Tracker

# Daftarkan Tracker ke admin site
@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'order_at')  # Kolom yang akan ditampilkan di daftar admin
    search_fields = ('user__username', 'food__name')  # Kolom yang bisa dicari
    list_filter = ('order_at',)  # Filter berdasarkan tanggal order
