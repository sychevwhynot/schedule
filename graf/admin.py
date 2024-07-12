from django.contrib import admin
from .models import Address, Schedule

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

class AddressAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]

admin.site.register(Address, AddressAdmin)
admin.site.register(Schedule)
