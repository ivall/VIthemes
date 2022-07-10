from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search', views.SearchView.as_view(), name='search_view'),
    path('panel', views.PanelView.as_view(), name='panel_view'),
    path('panel/approve', views.ApproveThemeView.as_view(), name='approve_theme_view'),
    path('themes/new', views.CreateThemeView.as_view(), name='create_theme'),
    path('themes/edit/<uuid:theme_uuid>', views.edit, name='edit_theme'),
    path('themes/my', views.MyThemes.as_view(), name='my_themes_view'),
    path('themes/<uuid:theme_uuid>/', views.ThemeView.as_view(), name='theme_view'),
    path('themes/<uuid:theme_uuid>/vote', views.VoteView.as_view(), name='vote_view')
]
