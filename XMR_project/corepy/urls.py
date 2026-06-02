from django.urls import path, re_path, include
from corepy import views

app_name = 'corepy'

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.signin, name='welcome'),
    path('login/', views.signin, name='login'),
    path('logout/', views.logoutapp, name='logout'),

    re_path(r'^dashboard/$', views.WelcomeView.as_view(), name='dashboard'),
    path('upload/', views.UploadView.as_view(), name='upload'),

    path('dashboard/site/<int:id>/', views.SiteView.as_view(), name='site-info'),

    path('site-chart-details/<int:id>/', views.site_chart_detail, name='site_chart_detail'),

    path('reports/', views.reports, name='reports'),
    path('fetch_site_data_report/', views.fetch_site_data_report, name='fetch_site_data_report'),

    path('site_exceedance/', views.site_exceedance_report, name='site_exceedance'),

    path('exceedance/', views.exc_reports, name='exceedance'),

    # public urls
    path('rtwqms/', views.PublicDashboardView.as_view(), name='rtwqms'),

    path('rtwqms/site/<int:id>/', views.NewSiteView.as_view(), name='site-details'),

    path('new_reports/', views.new_reports, name='new_reports'),
]