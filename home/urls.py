from django.urls import path, include 
from home import views 

urlpatterns = [
   path('', views.index1, name='login'),
   path('dashboard/', views.dashboard1, name='dashboard'),
   path('dashboard/profile/', views.profile, name='profile'),
   path('dashboard/all_profile/', views.all_profile, name='all_profile'),
   path('dashboard/add_profile/', views.create_profile, name='add_profile'),
   path('dashboard/create_client/', views.create_client, name='create_client'),
   path('dashboard/create_admin/', views.profile, name='create_admin'),
   path('dashboard/key_skill/', views.key_skill, name='key_skill'),
   path('dashboard/category/', views.category_view, name='category'),
   path('api/update_profile/', views.profile, name='update_profile'),
   path('api/update_my_profile/', views.profile, name='update_my_profile'),
   path('api/delete_profile/', views.profile, name='delete_profile'),
   path('logout', views.logout1, name='logout'),
]

# urls.py

from django.conf import settings
from django.conf.urls.static import static



    # Add media URL mapping for development environmen
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
