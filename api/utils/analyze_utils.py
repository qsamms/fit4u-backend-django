def analyze_sets(sets) -> dict:
    largest = -1
    rating_sum, rating_num = 0, 0

    for set in sets:
        largest = max(largest, set.get("volume"))
        rating_sum += set.get("rating")
        rating_num += 1

    return {
        "largest_weight": largest,
        "rating_num": rating_num,
        "rating_sum": rating_sum,
    }
