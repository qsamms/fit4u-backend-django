def analyze_sets(sets) -> dict:
    largest = -1
    rating_sum, count = 0, 0

    for set in sets:
        largest = max(largest, set.get("volume"))
        rating_sum += set.get("rating")
        count += 1

    return {
        "max_lift": largest,
        "count": count,
        "rating_sum": rating_sum,
    }
