from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Homepage is root-level here
    path('', views.home, name='home'),
    
    # Delegate everything store-related under /store/
    path('store/', include('store.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)