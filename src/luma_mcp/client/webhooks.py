"""Typed operations for managing Luma webhook subscriptions."""

from luma_mcp.client.base import LumaClient
from luma_mcp.models import webhooks as models


class WebhooksClient(LumaClient):
    async def list_webhooks(
        self, request: models.ListWebhooksRequest
    ) -> models.ListWebhooksResponse:
        return await self.request(
            "GET", "/v1/webhooks/list", request, models.ListWebhooksResponse
        )

    async def get_webhook(
        self, request: models.GetWebhookRequest
    ) -> models.GetWebhookResponse:
        return await self.request(
            "GET", "/v2/webhooks/get", request, models.GetWebhookResponse
        )

    async def create_webhook(
        self, request: models.CreateWebhookRequest
    ) -> models.CreateWebhookResponse:
        return await self.request(
            "POST", "/v2/webhooks/create", request, models.CreateWebhookResponse
        )

    async def update_webhook(
        self, request: models.UpdateWebhookRequest
    ) -> models.UpdateWebhookResponse:
        return await self.request(
            "POST", "/v2/webhooks/update", request, models.UpdateWebhookResponse
        )

    async def delete_webhook(
        self, request: models.DeleteWebhookRequest
    ) -> models.DeleteWebhookResponse:
        return await self.request(
            "POST", "/v1/webhooks/delete", request, models.DeleteWebhookResponse
        )
