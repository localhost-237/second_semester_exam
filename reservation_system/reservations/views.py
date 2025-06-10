# reservations/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Reservation, Table, Comment
from .serializers import ReservationSerializer, TableSerializer, CommentSerializer
from django.utils import timezone

class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TableReservationListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        table_id = self.kwargs['table_id']
        return Reservation.objects.filter(table_id=table_id, date__gte=timezone.now().date())

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        reservation_id = self.request.data.get('reservation')
        reservation = Reservation.objects.get(id=reservation_id)
        serializer.save(user=self.request.user, reservation=reservation)
