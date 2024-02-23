from api.utils import check_required_fields


def is_valid_workout(data):
    return (
        check_required_fields(data, required_fields=["workout"])
        and check_required_fields(
            data["workout"], required_fields=["name", "datetime", "exercises"]
        )
        and check_required_fields(
            data["workout"]["exercises"], required_fields=["name", "unit", "sets"]
        )
    )
