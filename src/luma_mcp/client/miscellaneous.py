"""Typed operations for Luma user, entity, place, and image APIs."""

from luma_mcp.client.base import LumaClient
from luma_mcp.models import miscellaneous as models


class MiscellaneousClient(LumaClient):
    async def get_self(self, request: models.GetSelfRequest) -> models.GetSelfResponse:
        return await self.request(
            "GET", "/v1/users/get-self", request, models.GetSelfResponse
        )

    async def lookup_entity(
        self, request: models.LookupEntityRequest
    ) -> models.LookupEntityResponse:
        return await self.request(
            "GET", "/v1/entities/lookup", request, models.LookupEntityResponse
        )

    async def search_places(
        self, request: models.SearchPlacesRequest
    ) -> models.SearchPlacesResponse:
        return await self.request(
            "GET", "/v1/places/search", request, models.SearchPlacesResponse
        )

    async def search_cover_images(
        self, request: models.SearchCoverImagesRequest
    ) -> models.SearchCoverImagesResponse:
        return await self.request(
            "GET", "/v1/images/search", request, models.SearchCoverImagesResponse
        )

    async def create_upload_url(
        self, request: models.CreateUploadUrlRequest
    ) -> models.CreateUploadUrlResponse:
        return await self.request(
            "POST",
            "/v1/images/create-upload-url",
            request,
            models.CreateUploadUrlResponse,
        )
