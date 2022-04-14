"""
analytics URL Configuration
"""

from typing import List

import audiences.urls as audiences
import campaigns.urls as campaigns
import cities.urls as cities
import clients.urls as clients
import countries.urls as countries
import events.urls as events
import metadata.urls as metadata
import metrics.urls as metrics
import pages.urls as pages
import products.urls as products
import reports.urls as reports
import states.urls as states
import subscriptions.urls as subscriptions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLResolver, include, path
from rest_framework.routers import DefaultRouter

api: DefaultRouter = DefaultRouter(trailing_slash=False)
api.registry.extend(audiences.api.registry)
api.registry.extend(countries.api.registry)
api.registry.extend(states.api.registry)
api.registry.extend(cities.api.registry)
api.registry.extend(campaigns.api.registry)
api.registry.extend(pages.api.registry)
api.registry.extend(metadata.api.registry)
api.registry.extend(metrics.api.registry)
api.registry.extend(events.api.registry)
api.registry.extend(products.api.registry)
api.registry.extend(clients.api.registry)
api.registry.extend(subscriptions.api.registry)

urlpatterns: List[URLResolver] = static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + [
    path("api/auth/", include("rest_framework.urls")),
    path("api/", include(api.urls)),
    path("admin/", admin.site.urls),
    path("", include(reports.urlpatterns))
]
