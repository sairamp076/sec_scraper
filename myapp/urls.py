from django.urls import path
from .views import *

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('process-cid', ProcessCIDView.as_view(), name='process-cid'),  # Add the POST API
    path('analyse-cid', AnalyseCIDView.as_view(), name='analyse-cid'),  # Add the POST API
]
