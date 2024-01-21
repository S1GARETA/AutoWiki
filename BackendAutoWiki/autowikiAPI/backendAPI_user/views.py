from django.http import HttpResponseNotFound

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import CustomUser, Favorite
from .serializer import CustomUserSerializer, FavoriteSerializer


# Create your views here.
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

class FavoriteListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Получение списка избранных объектов для текущего пользователя
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Создание нового избранного объекта с автоматическим заполнением пользователя
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Удаление объекта из избранного для текущего пользователя
        item_type = request.data.get('item_type')
        item_id = request.data.get('item_id')

        if item_type is not None and item_id is not None:
            try:
                favorite = Favorite.objects.get(user=request.user, item_type=item_type, item_id=item_id)
                favorite.delete()
                return Response({'success: Объект удалён из избраного'}, status=status.HTTP_204_NO_CONTENT)
            except Favorite.DoesNotExist:
                return Response({'error: Такого объекта не существует'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'item_type и item_id обязательны'}, status=status.HTTP_400_BAD_REQUEST)

class IsFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, item_type, item_id):
        # Проверка, есть ли объект в избранном у пользователя
        is_favorite = Favorite.objects.filter(
            user=request.user,
            item_type=item_type,
            item_id=item_id
        ).exists()

        return Response({'is_favorite': is_favorite})