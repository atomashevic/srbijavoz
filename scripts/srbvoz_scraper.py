#!/usr/bin/env python3
"""API-first Srbija Voz notice scraper.

Pulls notices from the WordPress REST API used by srbvoz.rs and falls back to the old
HTML page only if the API request fails.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from typing import Any

import requests

API_URL = "https://www.srbvoz.rs/wp-json/wp/v2/info_post?per_page=100"
STATION_API_URL = "https://w3.srbvoz.rs/redvoznje/api/stanica/"
TIMETABLE_URL = "https://w3.srbvoz.rs/redvoznje/info/sr"
HTML_URL = "https://www.srbvoz.rs/redvoznje"
DEFAULT_OUTPUT_PATH = "srbvoz_notices.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "sr,en-US;q=0.9,en;q=0.8",
}


def strip_html(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_date(iso_date: str) -> str:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.astimezone().strftime("%d.%m.%Y")


def fetch_api_notices(session: requests.Session) -> list[dict[str, Any]]:
    resp = session.get(API_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    items = resp.json()

    notices = []
    for item in items:
        title = strip_html(item.get("title", {}).get("rendered", ""))
        content = strip_html(item.get("content", {}).get("rendered", ""))
        date = item.get("date")
        notices.append(
            {
                "id": item.get("id"),
                "date": format_date(date) if date else None,
                "title": title,
                "content": content,
                "link": item.get("link"),
            }
        )
    return notices


def fetch_html_fallback(session: requests.Session) -> dict[str, Any]:
    resp = session.get(HTML_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return {
        "status": resp.status_code,
        "content_length": len(resp.text),
        "sample": resp.text[:1000],
    }


def fetch_station_matches(session: requests.Session, term: str) -> list[dict[str, Any]]:
    resp = session.get(
        STATION_API_URL,
        headers=HEADERS,
        params={"term": term},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_timetable_page_info(session: requests.Session) -> dict[str, Any]:
    resp = session.get(TIMETABLE_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return {
        "status": resp.status_code,
        "title_hint": "Timetable - Serbian Train",
        "content_length": len(resp.text),
        "has_station_api": "/api/stanica/" in resp.text,
        "has_train_details_api": "/api/vozdetalji1" in resp.text,
        "sample": resp.text[:1200],
    }


def matches_query(notice: dict[str, Any], query: str | None) -> bool:
    if not query:
        return True
    haystack = f"{notice.get('title', '')} {notice.get('content', '')}".lower()
    return query.lower() in haystack


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape Srbija Voz notices and timetable helpers.")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_PATH, help="Output JSON path")
    parser.add_argument("--limit", type=int, default=0, help="Limit the number of notices returned")
    parser.add_argument("--query", default="", help="Only keep notices containing this text")
    parser.add_argument("--station", default="", help="Also resolve station autocomplete matches for this term")
    parser.add_argument("--timetable-info", action="store_true", help="Also fetch timetable page metadata")
    parser.add_argument("--no-fallback", action="store_true", help="Do not use HTML fallback if API fails")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("=" * 60)
    print("Srbija Voz Notice Scraper")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    session = requests.Session()
    output: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "api-first",
        "api_url": API_URL,
        "html_url": HTML_URL,
        "timetable_url": TIMETABLE_URL,
        "station_api_url": STATION_API_URL,
        "query": args.query or None,
        "station_query": args.station or None,
    }

    try:
        print("\n1. Fetching notices from WordPress REST API...")
        notices = fetch_api_notices(session)
        notices = [n for n in notices if matches_query(n, args.query)]
        if args.limit and args.limit > 0:
            notices = notices[: args.limit]

        output["notices"] = notices
        output["count"] = len(notices)
        print(f"Fetched {len(notices)} notices from API.")
        for notice in notices[:5]:
            print(f"- {notice['date']} | {notice['title']}")

        if args.station:
            print("\n2. Resolving station autocomplete matches...")
            station_matches = fetch_station_matches(session, args.station)
            output["station_matches"] = station_matches
            print(f"Found {len(station_matches)} station matches for {args.station!r}.")
            for station in station_matches[:5]:
                print(f"- {station.get('naziv')} ({station.get('sifra')})")

        if args.timetable_info:
            print("\n3. Fetching timetable page metadata...")
            timetable_info = fetch_timetable_page_info(session)
            output["timetable_info"] = timetable_info
            print(f"Timetable page fetched, length: {timetable_info['content_length']}")

    except Exception as api_error:
        print(f"API fetch failed: {api_error}")
        if args.no_fallback:
            output["error"] = f"API error: {api_error}"
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            return 1

        print("\n2. Falling back to HTML page...")
        try:
            fallback = fetch_html_fallback(session)
            output["fallback"] = fallback
            print(f"Fallback succeeded, page length: {fallback['content_length']}")
        except Exception as html_error:
            output["error"] = f"API error: {api_error}; HTML error: {html_error}"
            print(f"Fallback failed: {html_error}")
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            return 1

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
