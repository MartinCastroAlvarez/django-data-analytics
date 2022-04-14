from typing import List

from django.urls import URLResolver, path

from reports.views import DashboardView

urlpatterns: List[URLResolver] = [
    path("", DashboardView.as_view(), name="dashboard"),
]
