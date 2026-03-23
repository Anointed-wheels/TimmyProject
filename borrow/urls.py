from django.urls import path
from . import views

urlpatterns = [
    path('borrow/<int:book_id>/', views.borrow_book, name="borrow_book"),
    path('my-borrows/', views.my_borrows, name='my_borrows'),
    path('approve-requests/', views.approve_requests, name='approve_requests'),
    path('approve-borrow/<int:id>/', views.approve_borrow, name='approve_borrow'),
    path("request/<int:book_id>/", views.request_book, name="request_book"),
    path("reserve/<int:book_id>/", views.reserve_book, name="reserve_book"),
]
