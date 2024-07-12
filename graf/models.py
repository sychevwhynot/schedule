from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Address(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day_of_week = models.CharField(max_length=20, editable=False)

    def __str__(self):
        return f"{self.user.username} - {self.address.name} - {self.date}"

    def save(self, *args, **kwargs):
        self.day_of_week = self.date.strftime('%A')
        super().save(*args, **kwargs)

    @property
    def get_day_display(self):
        if self.date:
            days = {
                'Monday': _('Понедельник'),
                'Tuesday': _('Вторник'),
                'Wednesday': _('Среда'),
                'Thursday': _('Четверг'),
                'Friday': _('Пятница'),
                'Saturday': _('Суббота'),
                'Sunday': _('Воскресенье'),
            }
            return days.get(self.date.strftime('%A'), _('Неизвестный день'))
        return _('Дата не задана')
