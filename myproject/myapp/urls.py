from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('add_recipe/', AddRecipe.as_view(), name='add_recipe'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recipe/<int:recipe_id>/', ShowRecipe.as_view(), name='recipe'),
    path('category/<int:cat_id>/', ShowCategory.as_view(), name='category')
]
