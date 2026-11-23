from statistics import mean, median
import redis


def _extract_name_from_record(record):
    """Extract a repository name from a dict, string, or tuple record."""
    if isinstance(record, str):
        cleaned = record.strip()
        return cleaned or None

    if isinstance(record, dict):
        for key in ("name", "repo_name", "repository_name", "full_name", "title"):
            val = record.get(key)
            if isinstance(val, str) and val.strip():
                name = val.strip()
                if key == "full_name" and "/" in name:
                    name = name.split("/", 1)[1].strip()
                return name or None

    return None


def _collect_repo_names(connection=None):
    """Collect repository names using existing project helpers when available."""
    names = []

    try:
        from redis_db.redis_menu import get_repositories_from_redis

        records = get_repositories_from_redis()
        if records:
            for item in records:
                extracted = _extract_name_from_record(item)
                if extracted:
                    names.append(extracted)
    except Exception:
        pass

    if not names and connection is not None:
        for key in connection.scan_iter(match="*"):
            key_type = connection.type(key)
            if key_type == "hash":
                data = connection.hgetall(key)
                extracted = _extract_name_from_record(data)
                if extracted:
                    names.append(extracted)
            elif key_type == "set":
                for member in connection.smembers(key):
                    extracted = _extract_name_from_record(str(member))
                    if extracted:
                        names.append(extracted)
            elif key_type == "string":
                val = connection.get(key)
                extracted = _extract_name_from_record(val)
                if extracted:
                    names.append(extracted)

    return names


def repository_name_length_analysis(connection=None):
    """Analyze repository name lengths from Redis and print a summary report."""
    names = _collect_repo_names(connection)
    if not names:
        print("\nNo repository records found for name-length analysis.")
        return

    lengths = [len(name) for name in names]
    min_len = min(lengths)
    max_len = max(lengths)

    short_count = sum(1 for n in lengths if n <= 10)
    medium_count = sum(1 for n in lengths if 11 <= n <= 25)
    long_count = sum(1 for n in lengths if n >= 26)

    shortest_names = sorted({name for name in names if len(name) == min_len})
    longest_names = sorted({name for name in names if len(name) == max_len})

    print("\n" + "=" * 50)
    print("       REPOSITORY NAME-LENGTH ANALYSIS")
    print("=" * 50)
    print(f"Repositories analyzed : {len(names)}")
    print(f"Shortest name length  : {min_len} chars ({', '.join(shortest_names)})")
    print(f"Longest name length   : {max_len} chars ({', '.join(longest_names)})")
    print(f"Average name length   : {mean(lengths):.2f} chars")
    print(f"Median name length    : {median(lengths):.2f} chars")
    print("-" * 50)
    print(f"Short  (1-10 chars)   : {short_count}")
    print(f"Medium (11-25 chars)  : {medium_count}")
    print(f"Long   (26+ chars)    : {long_count}")
    print("=" * 50)
