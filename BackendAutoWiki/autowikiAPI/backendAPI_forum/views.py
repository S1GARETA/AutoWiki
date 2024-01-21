from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import ForumPost, ForumComment
from .serializer import ForumPostSerializer, ForumOnePostSerializer, ForumCommentSerializer, ForumPostAllSerializer
from backendAPI_auto.models import Auto, Section

# Create your views here.

# ---- Посты ----

# Отобразить все посты определенной машины и её раздела
class ForumPostsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, car_brand, car_model, section_slug, post_id):
        try:
            post = ForumPost.objects.get(id=post_id)
            serializer = ForumOnePostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ForumPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            # Получите данные из тела запроса в формате JSON
            car_brand = request.data.get('car_brand', '')
            car_model = request.data.get('car_model', '')
            section_slug = request.data.get('section_slug', '')

            # Проверьте, что все необходимые поля присутствуют
            if not car_brand or not car_model or not section_slug:
                return Response({"error": "Марка, модель и раздел обязательны"}, status=400)

            # Получите список автомобилей по марке и модели
            autos = Auto.objects.filter(car_brand=car_brand, car_model=car_model)

            # Создайте список для хранения всех постов
            all_posts = []

            # Пройдитесь по всем найденным автомобилям
            for auto in autos:
                # Получите раздел по slug и инструкции для каждого автомобиля
                section = get_object_or_404(Section, slug=section_slug, instruction=auto.instruction)
                # Получите все посты для данного автомобиля и раздела
                posts = ForumPost.objects.filter(auto=auto, section=section)
                # Добавьте посты в общий список
                all_posts.extend(posts)

            # Сериализуйте данные всех постов для ответа
            serializer = ForumPostSerializer(all_posts, many=True)

            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

# Создание поста на форуме
class CreateForumPostView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Получите данные из тела запроса
            title = request.data.get('title', '')
            content = request.data.get('content', '')
            car_brand = request.data.get('car_brand', '')
            car_model = request.data.get('car_model', '')
            section_slug = request.data.get('section_slug', '')

            # Проверьте, что все необходимые поля присутствуют
            if not title or not content or not car_brand or not car_model or not section_slug:
                return Response({"error": "Заголовок, содержание, марка, модель и раздел обязательны"}, status=400)

            # Получите пользователя из JWT-токена
            user = request.user

            # Получите первый автомобиль по марке и модели
            auto = Auto.objects.filter(car_brand=car_brand, car_model=car_model).first()

            # Проверьте, что автомобиль был найден
            if not auto:
                return Response({"error": "Автомобиль не найден"}, status=404)

            # Получите раздел по slug
            section = get_object_or_404(Section, slug=section_slug, instruction=auto.instruction)

            # Создайте пост
            post = ForumPost.objects.create(
                title=title,
                content=content,
                user=user,
                auto=auto,
                section=section
            )

            # Сериализуйте данные поста для ответа
            serializer = ForumPostSerializer(post)

            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

# Показывать только посты пользователя

class ForumUserQuestionsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_questions = ForumPost.objects.filter(user=request.user)
        serializer = ForumPostAllSerializer(user_questions, many=True)
        return Response(serializer.data)


# ---- Комментарии ----

# Посмотреть все комментарии
class ForumCommentsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, post_id):
        try:
            comments = ForumComment.objects.filter(post_id=post_id)
            serializer = ForumCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ForumComment.DoesNotExist:
            return Response({'error': 'Comments not found'}, status=status.HTTP_404_NOT_FOUND)

# Создание комментария
class ForumCommentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            content = request.data.get('content', '')
            post_id = request.data.get('post_id', '')

            if not content or not post_id:
                return Response({"error": "Обязательно нужен комментарий для отправки"}, status=400)

            # Получение экземпляра ForumPost
            try:
                post = ForumPost.objects.get(id=post_id)
            except ForumPost.DoesNotExist:
                return Response({"error": "Пост с указанным post_id не найден"}, status=404)

            # Получите пользователя из JWT-токена
            user = request.user

            # Создание комментария
            comment = ForumComment.objects.create(
                post=post,
                content=content,
                user=user,
            )

            serializer = ForumCommentSerializer(comment)

            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)