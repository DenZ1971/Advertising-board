from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', AdvertCreate.as_view(), name='post_create'),
    path('create/<int:pk>/edite/', AdvertUpdate.as_view(), name='advert_edite'),
    path('create/<int:pk>/delete/', AdvertDelete.as_view(), name='advert_delete'),
    path('adverts_list/', AdvertsList.as_view(), name='adverts_list'),
    path('froala_editor/', include('froala_editor.urls')),
    path('<int:pk>', AdvertDetail.as_view(), name='advert_detail'),
    path('create_response/<int:pk>', ResponseCreate.as_view(), name='response_create'),
    path('response_list', ResponseList.as_view(), name='response_list'),
    path('response_list/advert/<int:pk>', ResponseAdvert.as_view(), name='response_advert_list'),
    path('response_list/<int:pk>', ResponseDetail.as_view(), name='response_detail'),
    path('create_response/<int:pk>/edite/', ResponseUpdate.as_view(), name='response_edite'),
    path('create_response/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('adverts_user_list/', AdvertsUserList.as_view(), name='adverts_user_list')
]
