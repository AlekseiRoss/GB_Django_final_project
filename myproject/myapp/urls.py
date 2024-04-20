from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('add_receip/', AddReceipView.as_view(), name='add_receip'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recipe/<int:recipe_id>/', RecipeView.as_view(), name='recipe'),
    path('category/<int:cat_id>/', ShowCategoryView.as_view(), name='category')
]
