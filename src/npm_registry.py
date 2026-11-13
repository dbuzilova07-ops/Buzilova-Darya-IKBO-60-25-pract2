"""Read public npm Registry metadata without using npm libraries."""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class NpmRegistry:
    """Fetch direct dependencies of latest npm package versions."""

    def __init__(self, base_url, timeout=12):
        """Store npm Registry base URL and create in-memory cache."""
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.cache = {}

    def dependencies(self, name):
        """Return a dict of direct runtime dependencies for a package."""
        if name not in self.cache:
            self.cache[name] = self._fetch_dependencies(name)
        return dict(self.cache[name])

    def _fetch_dependencies(self, name):
        """Read JSON metadata and extract dependencies from latest version."""
        url = f"{self.base_url}/{quote(name, safe='@')}"
        request = Request(
            url,
            headers={
                "Accept": "application/vnd.npm.install-v1+json",
                "User-Agent": "python-dependency-graph-lab/1.0",
            },
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                metadata = json.load(response)
        except HTTPError as error:
            raise ValueError(f"npm вернул HTTP {error.code}: {name}") from error
        except (URLError, OSError) as error:
            raise ValueError(f"Ошибка соединения с npm: {error}") from error
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("Некорректный ответ npm Registry") from error
        return latest_dependencies(metadata, name)


def latest_dependencies(metadata, name):
    """Select latest version and its declared runtime dependencies."""
    try:
        latest = metadata["dist-tags"]["latest"]
        dependencies = metadata["versions"][latest].get("dependencies", {})
    except (KeyError, TypeError) as error:
        raise ValueError(f"Нет данных о последней версии: {name}") from error
    if not isinstance(dependencies, dict):
        raise ValueError(f"Некорректные зависимости пакета: {name}")
    return dependencies
