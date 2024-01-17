"""REST client handling, including LightdashStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator


class LightdashStream(RESTStream):
    """Lightdash stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return '{url}/api/v1'.format(url=self.config["url"])

    records_jsonpath = "$.results[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        if self.config.get('personal_access_token') is not None:
            headers["Authorization"] = 'ApiKey {token}'.format(token=self.config['personal_access_token'])
        return headers

    @property
    def requests_session(self) -> requests.Session:
        # if not self._requests_session:
        self._requests_session = requests.Session()
        if self.config.get('username') is not None and self.config.get('password') is not None:
            _ = self._requests_session.post(
                '{url}/api/v1/login'.format(url=self.config['url']),
                json={
                    'email': self.config['username'],
                    'password': self.config['password'],
                },
                verify=False
            )
        return self._requests_session
