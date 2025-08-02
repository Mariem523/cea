from django.urls import path
from myapp.views.user_views import AdminCreationView, LoginView, AddUserView, UserListView, ResetUserPasswordView
from myapp.views.catalog_views import PublicCatalogListView,PrivateCatalogListView, CatalogCreateView,CatalogPDFDownloadView


urlpatterns = [
    path('api/admin/create/', AdminCreationView.as_view(), name='admin-create'),
    path('api/login/',        LoginView.as_view(),         name='api-login'),
    path('api/users/add/',    AddUserView.as_view(),       name='add-user'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/reset-password/', ResetUserPasswordView.as_view(), name='reset-user-password'),
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
]

