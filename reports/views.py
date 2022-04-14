import logging
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from reports.forms import DashboardForm
from reports.logic import ReportLogic

logger: logging.RootLogger = logging.getLogger(__name__)


class DashboardView(View):
    """
    Reports View
    """

    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        GET /dashboard
        """
        start: datetime = datetime.now() - timedelta(days=30)
        end: datetime = datetime.now()
        search: str = ""
        form: DashboardForm = DashboardForm(request.GET)
        if request.GET and form.is_valid():
            search: str = form.cleaned_data["search"]
            start: datetime = form.cleaned_data["start"]
            end: datetime = form.cleaned_data["end"]
        logic: ReportLogic = ReportLogic(
            start=start,
            end=end,
            search=search,
        )
        logger.debug("Dashboard: %s", logic)
        return render(
            request,
            "dashboard.html",
            {
                "form": form,
                "filters": {
                    "start": start,
                    "end": end,
                    "search": search,
                },
                "retention": {
                    "by_campaign": logic.get_retention_by_campaign(),
                    "by_product": logic.get_retention_by_product(),
                },
                "ltv": {
                    "by_campaign": logic.get_ltv_by_campaign(),
                },
                "margin": {
                    "by_month": logic.get_margin_by_month(),
                    "by_campaign": logic.get_margin_by_campaign(),
                },
                "events": {
                    "by_date": logic.get_events_by_date(),
                    "by_page": logic.get_events_by_page(),
                },
                "subscriptions": {
                    "by_date": logic.get_subscriptions_by_date(),
                    "by_campaign": logic.get_subscriptions_by_campaign(),
                    "by_audience": logic.get_subscriptions_by_audience(),
                    "by_product": logic.get_subscriptions_by_product(),
                    "by_city": logic.get_subscriptions_by_city(),
                    "by_state": logic.get_subscriptions_by_state(),
                    "by_country": logic.get_subscriptions_by_country(),
                    "by_dow_and_hod": logic.get_subscriptions_by_dow_and_hod(),
                    "by_dom": logic.get_subscriptions_by_dom(),
                    "by_moy": logic.get_subscriptions_by_moy(),
                },
            },
        )
