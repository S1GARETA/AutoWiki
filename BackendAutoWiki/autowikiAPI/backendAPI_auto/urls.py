from django.urls import path
from . import views
# from .views import AutoGetSlug

urlpatterns = [
    path('autolist/', views.AutoAPIList.as_view(), name='get_auto_list'), # Получить все машины
    path('autolist/brands/', views.AutoBrandsView.as_view(), name='get_brands_list'), # Получить только марки
    path('autolist/models/<str:car_brand>/', views.AutoModelsView.as_view(), name='get_models_list'), # Получить моделе по марке
    path('autolist/generations/<str:car_model>/', views.AutoGenerationsView.as_view(), name='get_generations_list'), # Получить поколения по моделе
    path('autolist/get-car-slug/', views.AutoGetSlug.as_view(), name='get_car_slug'), # Получить slug машины
    path('autolist/get-sections/', views.AutoSectionsView.as_view(), name='get_sections'), # Получить разделы машины

    path('autolist/<slug:car_slug>/', views.CarSectionsView.as_view(), name='get_sections_list'), # Получить секции инструкций
    path('autolist/<slug:car_slug>/<slug:section_slug>/', views.SubSectionsView.as_view(), name='get_content_subsections'), # Получить подразделы
    path('autolist/<slug:car_slug>/<slug:section_slug>/<int:subsection_id>/', views.SubSectionsView.as_view(), name='subsections_detail'), # Получить подразделы
]