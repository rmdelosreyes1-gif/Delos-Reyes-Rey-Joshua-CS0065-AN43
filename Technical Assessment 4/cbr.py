from knowledge_base import facts


# Task 3A - Build a Case Base
# Illustrative cases; replace them with observed problems and confirmed solutions.
coffee_cases = [
    {
        "problem": {"is_timer_set": False, "temperature": 90},
        "solution": "Set the timer.",
    },
    {
        "problem": {"water_level": 0.1, "is_timer_set": True},
        "solution": "Refill the water tank.",
    },
    {
        "problem": {"coffee_beans": 10, "temperature": 90},
        "solution": "Refill the coffee beans.",
    },
]

weather_cases = [
    {
        "problem": {
            "weather_temperature_celsius": 32,
            "weather_humidity_percentage": 85,
            "weather_is_raining": False,
        },
        "solution": "Stay hydrated and be cautious of the high humidity.",
    },
    {
        "problem": {
            "weather_is_raining": True,
            "weather_action_activate_sprinklers": True,
        },
        "solution": "Take an umbrella and leave the sprinklers off.",
    },
    {
        "problem": {
            "weather_cloud_presence": True,
            "weather_is_raining": False,
            "weather_temperature_celsius": 24,
        },
        "solution": "Check the forecast before going out.",
    },
]

user_cases = [
    {
        "problem": {
            "user_is_home": True,
            "user_is_sleeping": False,
            "user_is_working": True,
        },
        "solution": "Keep interruptions to a minimum while the user works.",
    },
    {
        "problem": {"user_health": 0.4, "user_mood": 0.5},
        "solution": "Suggest a break and a health check.",
    },
    {
        "problem": {"user_is_home": True, "user_is_sleeping": True},
        "solution": "Avoid disturbing the user.",
    },
]

environment_cases = [
    {
        "problem": {
            "environment_is_occupied": True,
            "environment_light_level": 0.5,
            "environment_temperature": 22,
            "environment_air_quality": 0.8,
        },
        "solution": "Keep the current environment settings.",
    },
    {
        "problem": {
            "environment_is_occupied": True,
            "environment_light_level": 0.2,
        },
        "solution": "Turn on the lights.",
    },
    {
        "problem": {"environment_air_quality": 0.3},
        "solution": "Use an air purifier.",
    },
]

sms_cases = [
    {
        "problem": {
            "sms_status": True,
            "sms_battery_level": 0.9,
            "sms_signal_strength": 0.8,
            "sms_connected_devices": 5,
            "sms_is_active": True,
        },
        "solution": "No maintenance is needed.",
    },
    {
        "problem": {"sms_status": True, "sms_battery_level": 0.1},
        "solution": "Charge the smart home system.",
    },
    {
        "problem": {"sms_status": False},
        "solution": "Check the smart home system connection.",
    },
]

case_bases = {
    "coffee_machine": coffee_cases,
    "weather": weather_cases,
    "user": user_cases,
    "environment": environment_cases,
    "sms": sms_cases,
}

# A numeric difference of this size gives a feature zero similarity.
numeric_scales = {
    "water_level": 1,
    "brew_strength": 1,
    "temperature": 40,
    "coffee_beans": 100,
    "weather_temperature_celsius": 50,
    "weather_humidity_percentage": 100,
    "user_health": 1,
    "user_mood": 1,
    "environment_light_level": 1,
    "environment_temperature": 40,
    "environment_noise_level": 1,
    "environment_air_quality": 1,
    "sms_battery_level": 1,
    "sms_signal_strength": 1,
    "sms_connected_devices": 20,
}


# Retrieval helper: find the most similar case before the reuse step.
def case_similarity(problem, current_facts):
    scores = []

    for key, past_value in problem.items():
        current_value = current_facts[key]

        # A contradictory Boolean fact makes this case inapplicable.
        if isinstance(past_value, bool):
            if current_value != past_value:
                return 0.0
            scores.append(1.0)
        else:
            scale = numeric_scales[key]
            scores.append(max(0.0, 1 - abs(current_value - past_value) / scale))

    return sum(scores) / len(scores)


def retrieve_case(cases, current_facts, minimum_similarity=0.8):
    best_case = max(
        cases,
        key=lambda case: (
            case_similarity(case["problem"], current_facts),
            len(case["problem"]),
        ),
        default=None,
    )

    if best_case is None:
        return None

    similarity = case_similarity(best_case["problem"], current_facts)
    if similarity < minimum_similarity:
        return None

    return {
        "solution": best_case["solution"],
        "similarity": round(similarity, 2),
        "matched_problem": best_case["problem"],
    }


# Task 3B - Reuse Step
# Return the solution of the most similar case.
def reuse_solution(retrieved_case):
    if retrieved_case is None:
        return None
    return retrieved_case["solution"]


# Task 3C - Revise Step
# Press Enter to keep the solution, or type a replacement.
def revise_solution(solution, adjustment=None):
    if solution is None:
        return None

    if adjustment is None:
        adjustment = input("Enter a revised solution (press Enter to keep it): ")

    return adjustment.strip() or solution


# Task 3D - Retain Step
# Add the current problem and its final solution to the case base.
def retain_case(cases, current_facts, solution):
    if not cases:
        raise ValueError("Cannot determine problem fields from an empty case base.")

    problem_keys = sorted({
        key for case in cases for key in case["problem"]
    })
    new_case = {
        "problem": {key: current_facts[key] for key in problem_keys},
        "solution": solution,
    }
    cases.append(new_case)
    return new_case


if __name__ == "__main__":
    print("Case-Based Reasoning Results:")
    print("-----------------------------")
    for domain, cases in case_bases.items():
        retrieved_case = retrieve_case(cases, facts)
        if retrieved_case is None:
            print(f"{domain}: No sufficiently similar case found.")
            continue

        solution = reuse_solution(retrieved_case)
        if solution is None:
            print(f"{domain}: No sufficiently similar case found.")
            continue

        print(
            f"{domain}: {solution} "
            f"(similarity: {retrieved_case['similarity']:.0%})"
        )
        final_solution = revise_solution(solution)
        retain_case(cases, facts, final_solution)
        print(f"Retained solution: {final_solution}")
