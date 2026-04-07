"""Handles user input and query-based image filtering."""

import datetime

# Earliest available APOD entry
EARLIEST_APOD_DATE = 19950616


def get_inputs() -> tuple[str, str, str]:
    """Prompt the user for a date range and search query.

    Returns:
        A tuple of (start_date, end_date, query) as strings.
    """
    start_date = _prompt_start_date()
    end_date = _prompt_end_date(start_date)
    query = _prompt_query()
    return start_date, end_date, query


def search_descriptions(results: list[dict], query: str) -> tuple[str, str]:
    """Score each APOD result against the query and return the two best image URLs.

    Each result's explanation is compared word-by-word against the query terms.
    The top two scoring image URLs are returned. YouTube links are excluded.

    Args:
        results: List of APOD result dicts from the NASA API.
        query: Space-separated search terms.

    Returns:
        A tuple of (best_url, second_best_url).
    """
    query_terms = set(query.lower().split())

    scored: list[tuple[int, str]] = []
    for entry in results:
        if "youtube" in entry.get("url", ""):
            continue
        explanation_words = entry.get("explanation", "").lower().split()
        score = sum(1 for word in explanation_words if word in query_terms)
        scored.append((score, entry["url"]))

    scored.sort(key=lambda item: item[0], reverse=True)

    if len(scored) < 2:
        raise ValueError("Not enough non-YouTube results to select two images.")

    return scored[0][1], scored[1][1]


# --- Private helpers ---


def _is_valid_date(date_string: str) -> bool:
    """Check whether a date string is a valid APOD date in YYYY-MM-DD format."""
    try:
        date = datetime.date.fromisoformat(date_string)
    except ValueError:
        return False

    today = datetime.date.today()
    earliest = datetime.date(1995, 6, 16)
    return earliest <= date <= today


def _prompt_start_date() -> str:
    """Prompt for a start date, returning empty string if skipped."""
    while True:
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        if not start_date:
            return ""
        if _is_valid_date(start_date):
            return start_date
        print("Invalid date. Must be YYYY-MM-DD between 1995-06-16 and today.")


def _prompt_end_date(start_date: str) -> str:
    """Prompt for an end date that falls on or after start_date."""
    while True:
        end_date = input("End date (YYYY-MM-DD): ").strip()
        if not end_date and not start_date:
            return ""
        if not _is_valid_date(end_date):
            print("Invalid date. Must be YYYY-MM-DD between 1995-06-16 and today.")
            continue

        reference = start_date if start_date else "2024-01-01"
        if end_date >= reference:
            return end_date
        print(f"End date must be on or after {reference}.")


def _prompt_query() -> str:
    """Prompt for a non-empty search query."""
    while True:
        query = input("Search query: ").strip()
        if query:
            return query.lower()
        print("Query cannot be empty.")
