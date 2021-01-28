"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from users import views as user_views
from climbguide import views
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # user URLS
    path('accounts/profile/', user_views.profile, name="profile"),
    path("accounts/", include("allauth.urls")),
    path('api-auth/', include('rest_framework.urls')),
    # climbguide URLS
    path('', views.home, name='home'),
    path('search/', views.search, name="search"),
        # routes
    path('routes/detail/<int:route_pk>', views.route_detail, name="route_detail"),
    path('routes/detail/<int:route_pk>/addphoto/', views.addphoto_to_route, name="addphoto_to_route"),
    path('routes/detail/<int:route_pk>/addcomment/', views.addcomment_to_route, name="addcomment_to_route"),
    path('routes/detail/<int:route_pk>/deletecomment/', views.deletecomment_from_route, name="deletecomment_from_route"),
        # daytrip
    path('daytrips/add/', views.add_daytrip, name="add_daytrip"),
    path('daytrips/detail/<int:daytrip_pk>', views.daytrip_detail, name="daytrip_detail"),
    path('daytrips/edit/<int:daytrip_pk>', views.edit_daytrip, name="edit_daytrip"),
    path('daytrips/delete/<int:daytrip_pk>', views.delete_daytrip, name="delete_daytrip"),
    path('daytrips/detail/<int:daytrip_pk>/addroutes/', views.addroutes_to_daytrip, name="addroutes_to_daytrip"),
    path('daytrips/detail/<int:daytrip_pk>/addlog/', views.addlog_to_daytrip, name="addlog_to_daytrip"),
    path('daytrips/detail/<int:daytrip_pk>/deletelog/', views.deletelog_from_daytrip, name="deletelog_from_daytrip"),

        # pointofinterest
    path('pointsofinterest/add/', views.add_pointofinterest, name="add_pointofinterest"),
    path('pointsofinterest/detail/<int:pointofinterest_pk>', views.pointofinterest_detail, name="pointofinterest_detail"),
    path('pointsofinterest/edit/<int:pointofinterest_pk>', views.edit_pointofinterest, name="edit_pointofinterest"),
    path('pointsofinterest/delete/<int:pointofinterest_pk>', views.delete_pointofinterest, name="delete_pointofinterest"),
    path('pointsofinterest/detail/<int:pointofinterest_pk>/addphoto/', views.addphoto_to_pointofinterest, name="addphoto_to_pointofinterest"),
    path('pointsofinterest/detail/<int:pointofinterest_pk>/addlocation/',views.addlocation_to_pointofinterest, name="add_poi_location"),    
# API URLS
    path("api/routes/", api_views.RouteSearchView.as_view()),
    path("api/daytrips/", api_views.DaytripListCreateView.as_view()),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
