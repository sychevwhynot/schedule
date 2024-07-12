from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import login_view, logout_view
from users.views import registration_view, CustomPasswordResetView


urlpatterns = [
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout' ),
    path('login/', login_view, name='login' ),
    path('password-reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/custom_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('', include('graf.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    print(f"Serving media files from {settings.MEDIA_URL} at {settings.MEDIA_ROOT}")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)