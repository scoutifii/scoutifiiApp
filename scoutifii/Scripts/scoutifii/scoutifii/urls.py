
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from two_factor.urls import urlpatterns as tf_urls
from graphene_django.views import GraphQLView

urlpatterns = [
    path('scoutifii-admin-login/', admin.site.urls),
    # path('', include('tf_urls')),
    path('', include('scoutifiiapp.urls')), 
    path("graphql", GraphQLView.as_view(graphiql=True))   
]

# Specifying URL for our media and static root like file uploads

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
