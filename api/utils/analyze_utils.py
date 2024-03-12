def standardize_weight(w, r) -> int:
    # using McGlothlin formula: https://www.fxsolver.com/browse/formulas/One-repetition+maximum+%28McGlothin+formula%29
    return int((100 * w) / (101.3 - (2.67123 * r)))


def analyze_sets(sets: list, unit: str) -> dict:
    largest = -1
    rating_sum, count = 0, 0

    for set in sets:
        volume = set.get("reps") if unit == "bw" else set.get("volume")
        rating = set.get("rating")

        if type(volume) == str:
            volume = 0 if len(volume) == 0 else int(volume)

        if type(rating) == str:
            rating = 0 if len(rating) == 0 else int(rating)

        if unit == "lbs":
            # convert to kg for McGlothlin formula then back to lbs
            kg = volume / 2.205
            volume = int(standardize_weight(kg, set.get("reps")) * 2.205)
        elif unit == "kg":
            volume = standardize_weight(volume, set.get("reps"))

        largest = max(largest, volume)
        rating_sum += rating
        count += 1

    return {
        "max_lift": largest,
        "count": count,
        "rating_sum": rating_sum,
    }
