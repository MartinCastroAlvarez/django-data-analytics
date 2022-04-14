import logging
from datetime import datetime
from typing import List

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pages.logic import PageLogic
from pages.models import Page
from pages.serializers import PageSerializer

logger: logging.RootLogger = logging.getLogger(__name__)


class PageViewSet(ModelViewSet):
    """
    Page Model API View.
    """

    queryset: QuerySet = Page.objects.all()
    serializer_class: type = PageSerializer

    def list(self, request: Request) -> Response:
        """
        GET /pages
        """
        pages: QuerySet = self.get_queryset()
        if any(
            [
                request.query_params.get("search"),
                request.query_params.get("start"),
                request.query_params.get("end"),
            ]
        ):
            pages: QuerySet = Page.active.search(
                search=request.query_params.get("search"),
                start=request.query_params.get("start"),
                end=request.query_params.get("end"),
            )
        serializer: PageSerializer = self.serializer_class(
            pages, many=True, context={"request": request}
        )
        logger.debug("List: %s", pages)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        """
        POST /pages
        """
        serializer: PageSerializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            page: Page = serializer.save()
            logic: PageLogic = PageLogic(page)
            logic.update_metadata()
            logger.debug("Created: %s", page)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        GET /pages/:int
        """
        page: Page = self.get_object()
        serializer: PageSerializer = self.serializer_class(
            page, context={"request": request}
        )
        logger.debug("Details: %s", page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int) -> Response:
        """
        PUT /pages/:int
        """
        page: Page = self.get_object()
        serializer: PageSerializer = self.serializer_class(
            page, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            page: Page = serializer.save()
            logic: PageLogic = PageLogic(page)
            logic.update_metadata()
            logger.debug("Updated: %s", page)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request: Request, pk: int) -> Response:
        """
        DELETE /pages/:int
        """
        page: Page = self.get_object()
        page.deleted_at = datetime.now()
        page.save()
        page.metadata.deleted_at = datetime.now()
        page.metadata.save()
        serializer: PageSerializer = self.serializer_class(
            page, context={"request": request}
        )
        logger.debug("Deleted: %s", page)
        return Response(serializer.data, status=status.HTTP_200_OK)
