def analyze_sets(sets) -> dict:
    largest = -1
    rating_sum, count = 0, 0

    for set in sets:
        volume = set.get("volume")
        rating = set.get("rating")

        if type(volume) == str:
            volume = 0 if len(volume) == 0 else int(volume)

        if type(rating) == str:
            rating = 0 if len(rating) == 0 else int(rating)

        largest = max(largest, volume)
        rating_sum += rating
        count += 1

    return {
        "max_lift": largest,
        "count": count,
        "rating_sum": rating_sum,
    }
