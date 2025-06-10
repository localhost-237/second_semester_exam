from rest_framework import serializers
from .models import Reservation, Comment
from django.utils import timezone

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'status')

    def validate(self, data):
        # Check if end time is after start time
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time")

        # Check if reservation is in the future
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("Reservation date must be in the future")

        # Check guest count doesn't exceed table capacity
        if data['guest_count'] > data['table'].capacity:
            raise serializers.ValidationError(f"Guest count exceeds table capacity (max {data['table'].capacity})")

        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def validate_content(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Comment cannot be empty")
        if len(value) > 1000:
            raise serializers.ValidationError("Comment cannot exceed 1000 characters")
        return value

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
