from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    """Represents a restaurant table"""
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    location = models.CharField(max_length=100)  # e.g., 'Window', 'Patio', 'Main Hall'

    def __str__(self):
        return f"Table {self.number} ({self.capacity} seats)"

class Reservation(models.Model):
    """Represents a reservation made by a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guest_count = models.IntegerField()
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], default='confirmed')

    class Meta:
        unique_together = ('table', 'date', 'start_time')

    def __str__(self):
        return f"Reservation #{self.id} for {self.user.username}"

class Comment(models.Model):
    """User comments about their reservation experience"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.reservation}"
