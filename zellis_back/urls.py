from django.urls import path
from myapp.views.user_views import AdminCreationView, LoginView, AddUserView, UserListView, ResetUserPasswordView,CSRFView,MeView,LogoutView
from myapp.views.catalog_views import PublicCatalogListView,PrivateCatalogListView, CatalogCreateView,CatalogPDFDownloadView
from myapp.views.collection_views import CollectionCreateView,CollectionListView
from myapp.views.format_views import FormatCreateView, FormatViewSet, CollectionFormatsListView
from myapp.views.theme_views import ThemeCreateView, ThemesWithColorsByCollectionView,ThemesWithColorsByFormatView
from myapp.views.color_views import ColorCreateView
from django.conf import settings
from django.conf.urls.static import static

format_list = FormatViewSet.as_view({'get': 'list'})      # add this
format_detail = FormatViewSet.as_view({
    'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy',
})

urlpatterns = [
    path('api/admin/create/', AdminCreationView.as_view(), name='admin-create'),
    path('api/login/',        LoginView.as_view(),         name='api-login'),
    path('api/users/add/',    AddUserView.as_view(),       name='add-user'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/reset-password/', ResetUserPasswordView.as_view(), name='reset-user-password'),
    path('api/auth/csrf',   CSRFView.as_view()),
    #path('api/auth/login',  LoginView.as_view()),
    path('api/auth/me',     MeView.as_view()),
    path('api/auth/logout', LogoutView.as_view()),

    path("api/catalogs/public/",  PublicCatalogListView.as_view(),  name="catalogs-public"),
    path("api/catalogs/private/", PrivateCatalogListView.as_view(), name="catalogs-private"),
    path(
        'api/catalogs/add/',
        CatalogCreateView.as_view(),
        name='catalog-create'
    ),
    path(
        'api/catalogs/<int:pk>/download/',
        CatalogPDFDownloadView.as_view(),
        name='catalog-pdf-download'
    ),
    path('api/collections/create/', CollectionCreateView.as_view(), name='collection-create'),
    path('api/collections/', CollectionListView.as_view(), name='collection-list'),
    path('api/collections/<int:collection_id>/formats/',                          # ← ADD THIS
         CollectionFormatsListView.as_view(),
         name='collection-format-list'),
    # path('collections/', CollectionCreateView.as_view(), name='collections-create'),
    path('api/formats/', format_list, name='format-list'),  
    path('api/formats/create/', FormatCreateView.as_view(), name='formats-create'),
    path('api/themes/create/', ThemeCreateView.as_view(), name='themes-create'),
    path('api/colors/create/', ColorCreateView.as_view(), name='colors-create'),
    path(
        'api/collections/<int:collection_id>/themes-with-colors/',
        ThemesWithColorsByCollectionView.as_view(),
        name='themes-with-colors-by-collection'
    ),
    # Collection with formats
    path(
        'api/collections/<int:collection_id>/formats/<int:format_id>/themes-with-colors/',
        ThemesWithColorsByFormatView.as_view(),
        name='themes-with-colors-by-format'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


