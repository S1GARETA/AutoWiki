from django.urls import path
from . import views

urlpatterns = [
    path('forum/create-post/', views.CreateForumPostView.as_view(), name='create-post'), # Создать пост
    path('forum/posts/', views.ForumPostsView.as_view(), name='all-posts'), # Выдать все посты по авто и разделу
    path('forum/user-questions/', views.ForumUserQuestionsView.as_view(), name='user-questions'),

    path('forum/comments/create/', views.ForumCommentCreateView.as_view(), name='forum-comment-create'), # Создать комментарий
    path('forum/comments/<int:post_id>/', views.ForumCommentsView.as_view(), name='forum-comments-list'), # Получить все комментарии

    path('forum/<str:car_brand>/<str:car_model>/<slug:section_slug>/<int:post_id>/', views.ForumPostsView.as_view(), name='forum-post-detail'), # Получить один пост
]