"""Validation helpers for repository identifiers and watch counts."""

import re

_REPOSITORY_NAME_PATTERN = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}/[A-Za-z0-9._-]{1,100}\Z"
)


def validate_repository_name(repo_name: object) -> str:
    """Return a trimmed owner/repository name containing only safe characters."""
    if not isinstance(repo_name, str):
        raise ValueError("Repository name must be text in owner/repository format.")

    normalized_name = repo_name.strip()
    if not _REPOSITORY_NAME_PATTERN.fullmatch(normalized_name):
        raise ValueError(
            "Repository name must use owner/repository format and contain "
            "only letters, numbers, periods, underscores, or hyphens."
        )

    return normalized_name


def validate_watch_count(watch_count: object) -> int:
    """Require a nonnegative integer watch count (excluding booleans)."""
    if not isinstance(watch_count, int) or isinstance(watch_count, bool):
        raise ValueError("Watch count must be an integer.")
    if watch_count < 0:
        raise ValueError("Watch count cannot be negative.")

    return watch_count


def parse_watch_count(watch_count: object) -> int:
    """Convert numeric strings and validate nonnegative watch counts."""
    if isinstance(watch_count, str):
        watch_count = watch_count.strip()

        if not re.fullmatch(r"[0-9]+", watch_count):
            raise ValueError("Watch count must be a nonnegative integer.")

        watch_count = int(watch_count)

    return validate_watch_count(watch_count)
