"""Stream type classes for tap-lightdash."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_lightdash.client import LightdashStream


class ProjectsStream(LightdashStream):
    name = "projects"
    path = "/org/projects"
    primary_keys = ["projectUuid"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("projectUuid", th.StringType),
        th.Property("type", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        return {
            "projectUuid": record["projectUuid"],
        }


# TODO: Will needs updates for non-Snowflake warehouses and non-Github dbt connections
class ProjectDetailsStream(LightdashStream):
    name = "project_details"
    path = "/projects/{projectUuid}"
    primary_keys = ["projectUuid"]
    parent_stream_type = ProjectsStream
    ignore_parent_replication_keys = True
    replication_key = None
    schema = th.PropertiesList(
        th.Property("organizationUuid", th.StringType),
        th.Property("projectUuid", th.StringType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),
        th.Property("dbtConnection", th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("repository", th.StringType),
            th.Property("branch", th.StringType),
            th.Property("project_sub_path", th.StringType),
            th.Property("host_domain", th.StringType),
        )),
        th.Property("warehouseConnection", th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("account", th.StringType),
            th.Property("role", th.StringType),
            th.Property("database", th.StringType),
            th.Property("warehouse", th.StringType),
            th.Property("schema", th.StringType),
            th.Property("clientSessionKeepAlive", th.BooleanType),
            th.Property("threads", th.NumberType),
        )),
    ).to_dict()


class ProjectTablesConfigurationStream(LightdashStream):
    name = "project_tables_configuration"
    path = "/projects/{projectUuid}/tablesConfiguration"
    primary_keys = ["projectUuid"]
    parent_stream_type = ProjectsStream
    ignore_parent_replication_keys = True
    replication_key = None
    schema = th.PropertiesList(
        th.Property("projectUuid", th.StringType),
        th.Property("tableSelection", th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("value", th.StringType),
        )),
    ).to_dict()


class ProjectDashboardsStream(LightdashStream):
    name = "project_dashboards"
    path = "/projects/{projectUuid}/dashboards"
    primary_keys = ["projectUuid", "uuid"]
    parent_stream_type = ProjectsStream
    ignore_parent_replication_keys = True
    replication_key = None
    schema = th.PropertiesList(
        th.Property("organizationUuid", th.StringType),
        th.Property("projectUuid", th.StringType),
        th.Property("uuid", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("spaceUuid", th.StringType),
        th.Property("updatedByUser", th.ObjectType(
            th.Property("userUuid", th.StringType),
            th.Property("firstName", th.StringType),
            th.Property("lastName", th.StringType),
        )),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        return {
            "dashboardUuid": record["uuid"],
        }


class DashboardsStream(LightdashStream):
    name = "dashboards"
    path = "/dashboards/{dashboardUuid}"
    primary_keys = ["uuid"]
    parent_stream_type = ProjectDashboardsStream
    ignore_parent_replication_keys = True
    replication_key = None
    schema = th.PropertiesList(
        th.Property("organizationUuid", th.StringType),
        th.Property("projectUuid", th.StringType),
        th.Property("uuid", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("spaceUuid", th.StringType),
        th.Property("spaceName", th.StringType),
        th.Property("tiles", th.ArrayType(
            th.ObjectType(
                th.Property("uuid", th.StringType),
                th.Property("type", th.StringType),
                th.Property("properties", th.ObjectType(
                    th.Property("savedChartUuid", th.StringType),
                    th.Property("title", th.StringType),
                    th.Property("url", th.StringType),
                    th.Property("content", th.StringType),
                )),
                th.Property("x", th.NumberType),
                th.Property("y", th.NumberType),
                th.Property("h", th.NumberType),
                th.Property("w", th.NumberType),
            )
        )),
        th.Property("filters", th.ObjectType(
            th.Property("metrics", th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("operator", th.StringType),
                    th.Property("target", th.ObjectType(
                        th.Property("fieldId", th.StringType),
                        th.Property("tableName", th.StringType),
                    )),
                )
            )),
            th.Property("dimensions", th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("operator", th.StringType),
                    th.Property("target", th.ObjectType(
                        th.Property("fieldId", th.StringType),
                        th.Property("tableName", th.StringType),
                    )),
                )
            )),
        )),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        return {
            "savedChartUuids": [tile["properties"]["savedChartUuid"] for tile in record["tiles"] if tile.get("properties", {}).get("savedChartUuid")],
        }


class SavedChartStream(LightdashStream):
    name = "saved_charts"
    path = "/saved/{savedChartUuid}"
    primary_keys = ["uuid"]
    state_partitioning_keys = ["uuid"]
    parent_stream_type = DashboardsStream
    ignore_parent_replication_keys = True
    replication_key = None
    schema = th.PropertiesList(
        th.Property("organizationUuid", th.StringType),
        th.Property("projectUuid", th.StringType),
        th.Property("spaceUuid", th.StringType),
        th.Property("spaceName", th.StringType),
        th.Property("uuid", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("tableName", th.StringType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("firstViewedAt", th.DateTimeType),
        th.Property("updatedByUser", th.ObjectType(
            th.Property("userUuid", th.StringType),
            th.Property("firstName", th.StringType),
            th.Property("lastName", th.StringType),
        )),
        ## Haven't added all of the below metricQuery yet
        th.Property("metricQuery", th.ObjectType(
            th.Property("dimensions", th.ArrayType(th.StringType)),
            th.Property("metrics", th.ArrayType(th.StringType)),
            th.Property("filters", th.ObjectType(
                th.Property("dimensions", th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("and", th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property("target", th.ObjectType(
                                th.Property("fieldId", th.StringType)
                            )),
                            th.Property("operator", th.StringType),
                        )
                    )),
                ))
            )),
        )),
        th.Property("views", th.IntegerType)
    ).to_dict()

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        Each record emitted should be a dictionary of property names to their values.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            One item per (possibly processed) record in the API.
        """
        for savedChartUuid in context["savedChartUuids"]:
            context["savedChartUuid"] = savedChartUuid
            for record in self.request_records(context):
                transformed_record = self.post_process(record, context)
                if transformed_record is None:
                    # Record filtered out during post_process()
                    continue
                yield transformed_record


class UsersStream(LightdashStream):
    name = "users"
    path = "/org/users"
    primary_keys = ["userUuid"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("userUuid", th.StringType),
        th.Property("firstName", th.StringType),
        th.Property("lastName", th.StringType),
        th.Property("email", th.StringType),
        th.Property("organizationUuid", th.StringType),
        th.Property("role", th.StringType),
        th.Property("isActive", th.BooleanType),
        th.Property("isInviteExpired", th.BooleanType),
    ).to_dict()

