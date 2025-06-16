from django.urls import path, include
from rest_framework import routers
from . import views
from . import rest_view

# router = routers.DefaultRouter()
# router.register(r'test', ApiTest)

urlpatterns = [
    path('', views.indexSlugless, name='index-slugless'),
    # path('upload', views.upload, name="upload"), # upload va prima di <slug:slug> altrimenti upload dimenta uno slug
    path('upload', views.UploadView.as_view(), name="upload"),
    path('search', views.search, name='search'),
    path('<slug:slug>', views.index, name='index'),
    path('artist/<slug:artist_slug>', views.artist_page, name='artist-page'),
    path('album/<slug:album_slug>', views.album_page, name='album-page'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),

    # path('api/', include(router.urls)),
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

## urls.py (aggiungi sotto alle altre rotte api)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# Registrazione dei ViewSet
router.register(r'artists', rest_view.ArtistViewSet, basename='artist')
router.register(r'albums', rest_view.AlbumViewSet, basename='album')
router.register(r'tracks', rest_view.TrackViewSet, basename='track')


urlpatterns += [
    # path('api/test-audio/', rest_view.test_audio_endpoint, name='test-audio'),
    # path('api/', rest_view.IndexSluglessAPI.as_view(), name='api-index'),
    # path('api/<slug:slug>/', rest_view.ResourceListAPI.as_view(), name='api-resources'),
    # path('api/artist/<slug:artist_slug>/', rest_view.ArtistDetailAPI.as_view(), name='api-artist'),
    # path('api/album/<slug:album_slug>/', rest_view.AlbumDetailAPI.as_view(), name='api-album'),
    # path('api/search/', rest_view.SearchAPI.as_view(), name='api-search'),
    # path('api/upload/', rest_view.UploadAPI.as_view(), name='api-upload'),
    # path('api/login/', rest_view.LoginAPI.as_view(), name='api-login'),
    # path('api/logout/', rest_view.LogoutAPI.as_view(), name='api-logout'),
    path('api/', include(router.urls)),

]