from django.urls import path
from djapp.views import MyObtainTokenPairView, RegisterView, FileUploadView, FileListView, FileDownloadView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/upload/', FileUploadView.as_view(), name='file_upload'),
    path('api/download/', FileListView.as_view(), name='file_list'),
    path('api/download/<str:file_name>', FileDownloadView.as_view(), name='file_download'),
]