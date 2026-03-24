from django.urls import path
from . import views

urlpatterns = [
    path("request/<int:book_id>/", views.request_borrow, name="request_borrow"),
    path("my-borrows/", views.my_borrows, name="my_borrows"),
    path("manage/", views.manage_requests, name="manage_requests"),
    path("approve/<int:request_id>/", views.approve_request, name="approve_request"),
    path("reject/<int:request_id>/", views.reject_request, name="reject_request"),
    path("return/<int:request_id>/", views.mark_returned, name="mark_returned"),
    path("cancel/<int:request_id>/", views.cancel_request, name="cancel_request")
]
