# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import   create_deal, deal_detail, update_deal

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('create_deal/',create_deal, name='create_deal'),
    path('deal/<uuid:deal_id>/', deal_detail, name='deal_detail'),
    path('update_deal/', update_deal, name='update_deal'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
