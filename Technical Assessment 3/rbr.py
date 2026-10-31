from knowledge_base import facts

# Task 2A - 3 IF-THEN Rules

def check_coffee_machine(facts):
    if facts["water_level"] < 0.2:
        return "Refill water tank."
    elif facts["brew_strength"] < 0.5:
        return "Adjust brew strength."
    elif not facts["is_timer_set"]: # if the timer is not set
        return "Set the timer."
    elif facts["temperature"] < 85:
        return "Heat the water."
    elif facts["coffee_beans"] < 20:
        return "Refill coffee beans."
    else:
        return "Coffee machine is ready."


def check_weather(facts):
    if facts["weather_is_raining"]:
        return "Take an umbrella."
    elif facts["weather_temperature_celsius"] > 30:
        return "It's hot outside, stay hydrated."
    elif facts["weather_humidity_percentage"] > 80:
        return "High humidity, be cautious."
    elif facts["weather_cloud_presence"]:
        return "Cloudy weather, might rain later."
    elif facts["weather_action_activate_sprinklers"]:
        return "Activating sprinklers."
    else:
        return "Weather is great today! Enjoy your day."

def check_user(facts):
    if facts["user_is_home"] and not facts["user_is_sleeping"]:
        return "User is awake and at home."
    elif facts["user_is_working"]:
        return "User is working."
    elif facts["user_health"] < 0.5:
        return "User's health is low, consider taking a break."
    elif facts["user_mood"] < 0.5:
        return "User's mood is low, consider doing something enjoyable."
    else:
        return "User is in good condition."
    
def check_environment(facts):
    if facts["environment_is_occupied"]:
        return "Environment is occupied."
    elif facts["environment_light_level"] < 0.3:
        return "Environment is too dark, consider turning on lights."
    elif facts["environment_temperature"] < 18:
        return "Environment is too cold, consider adjusting the thermostat."
    elif facts["environment_noise_level"] > 0.7:
        return "Environment is too noisy, consider using noise-cancelling measures."
    elif facts["environment_air_quality"] < 0.5:
        return "Environment air quality is poor, consider using an air purifier."
    else:
        return "Environment is comfortable."

def check_sms(facts):
    if not facts["sms_status"]:
        return "Smart home system is offline."
    elif facts["sms_battery_level"] < 0.2:
        return "Smart home system battery is low, consider charging."
    elif facts["sms_signal_strength"] < 0.5:
        return "Smart home system signal is weak, consider moving closer to the router."
    elif facts["sms_connected_devices"] > 10:
        return "Too many devices connected to the smart home system, consider disconnecting some."
    elif not facts["sms_is_active"]:
        return "Smart home system is inactive, consider activating it."
    else:
        return "Smart home system is functioning properly."
    
# Task 2B - Implementing an Inference Engine
def inference_engine(facts):
    coffee_machine_status = check_coffee_machine(facts)
    weather_status = check_weather(facts)
    user_status = check_user(facts)
    environment_status = check_environment(facts)
    sms_status = check_sms(facts)

    return {
        "coffee_machine_status": coffee_machine_status,
        "weather_status": weather_status,
        "user_status": user_status,
        "environment_status": environment_status,
        "sms_status": sms_status
    }

#Task 2C - Display Output
def display_output(facts):
    inference_results = inference_engine(facts)
    
    print("Routine Check Results:")
    print("-------------------------")
    for key, value in inference_results.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")

if __name__ == "__main__":
    display_output(facts)