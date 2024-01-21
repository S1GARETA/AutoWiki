from django.urls import path
from . import views

urlpatterns = [
    path('users-list/', views.UserListView.as_view(), name='get_users_list'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/is_favorite/<str:item_type>/<int:item_id>/', views.IsFavoriteAPIView.as_view(), name='is-favorite'),
]