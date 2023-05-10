from django.urls import path

from .views import homePageView, noteAddView, noteView, noteDelete

urlpatterns = [
    path('', homePageView, name='home'),
    path('notes', noteAddView, name='addNote'),
    path('notes/<int:note_id>/', noteView, name='noteView'),
    path("notes/<int:note_id>/delete/", noteDelete, name="noteDelete"),
]
