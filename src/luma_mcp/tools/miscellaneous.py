"""MCP tools for Luma identity, entity lookup, places, and images."""

from mcp.server.mcpserver import Context, MCPServer
from mcp.types import ToolAnnotations

from luma_mcp.models import miscellaneous as models
from luma_mcp.tools.context import miscellaneous_client


async def get_self(
    request: models.GetSelfRequest, ctx: Context
) -> models.GetSelfResponse:
    "Return the Luma user authenticated by the caller's API key."
    async with miscellaneous_client(ctx) as client:
        return await client.get_self(request)


async def lookup_entity(
    request: models.LookupEntityRequest, ctx: Context
) -> models.LookupEntityResponse:
    "Look up an event or calendar by its slug, Luma URL, or permanent public path such as `event/evt-...`, `e/evt-...`, or `calendar/cal-...`. URL query parameters and fragments are ignored."
    async with miscellaneous_client(ctx) as client:
        return await client.lookup_entity(request)


async def search_places(
    request: models.SearchPlacesRequest, ctx: Context
) -> models.SearchPlacesResponse:
    'Search Google Maps for a place and get up to 5 candidates. Pass the chosen `place_id` as `geo_address_json: { type: "google", place_id }` when creating or updating an event.'
    async with miscellaneous_client(ctx) as client:
        return await client.search_places(request)


async def search_cover_images(
    request: models.SearchCoverImagesRequest, ctx: Context
) -> models.SearchCoverImagesResponse:
    "Search Luma’s gallery of stock event cover images by keyword. Pass the chosen `image_url` as `cover_url` when creating or updating an event — gallery images don’t need to be uploaded first."
    async with miscellaneous_client(ctx) as client:
        return await client.search_cover_images(request)


async def create_upload_url(
    request: models.CreateUploadUrlRequest, ctx: Context
) -> models.CreateUploadUrlResponse:
    "Create a presigned URL for a separate image PUT upload and return its public file URL."
    async with miscellaneous_client(ctx) as client:
        return await client.create_upload_url(request)


OPERATIONS = [
    (get_self, True),
    (lookup_entity, True),
    (search_places, True),
    (search_cover_images, True),
    (create_upload_url, False),
]


def register_miscellaneous(server: MCPServer) -> None:
    for operation, read_only in OPERATIONS:
        server.tool(
            annotations=ToolAnnotations(
                read_only_hint=read_only,
                destructive_hint=not read_only,
                idempotent_hint=read_only,
                open_world_hint=True,
            ),
        )(operation)
