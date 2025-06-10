# reservations/urls.py
from django.urls import path
from .views import ReservationCreateView, TableReservationListView, CommentCreateView

urlpatterns = [
    path('reservations/', ReservationCreateView.as_view(), name='create-reservation'),
    path('tables/<int:table_id>/reservations/', TableReservationListView.as_view(), name='table-reservations'),
    path('comments/', CommentCreateView.as_view(), name='create-comment'),
]
