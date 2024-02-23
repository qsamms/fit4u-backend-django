from api.utils import check_required_fields


def is_valid_workout_plan(data):
    return check_required_fields(
        data, required_fields=["workout_plan"]
    ) and check_required_fields(
        data["workout_plan"], required_fields=["name", "exercises"]
    )
