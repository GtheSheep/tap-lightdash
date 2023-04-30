"""Lightdash tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_lightdash.streams import (
    ProjectsStream,
    ProjectDetailsStream,
    ProjectTablesConfigurationStream,
    ProjectDashboardsStream,
    DashboardsStream,
    SavedChartStream,
    UsersStream,
)
STREAM_TYPES = [
    ProjectsStream,
    ProjectDetailsStream,
    ProjectTablesConfigurationStream,
    ProjectDashboardsStream,
    DashboardsStream,
    SavedChartStream,
    UsersStream,
]


class TapLightdash(Tap):
    name = "tap-lightdash"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "personal_access_token",
            th.StringType,
            required=False,
            description="Personal access token to authenticate against the API service"
        ),
        th.Property(
            "username",
            th.StringType,
            required=False,
            description="Username to authenticate with"
        ),
        th.Property(
            "password",
            th.StringType,
            required=False,
            description="Password for authentication"
        ),
        th.Property(
            "url",
            th.StringType,
            required=True,
            description="URL of your Lightdash instance"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
