import os
import platform
import datetime as dt
import requests
import weather_config
import pytz

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def clear_screen():
    os_name = platform.system().lower()
    if os_name == "windows":
        os.system("cls")
    else:
        os.system("clear")

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * 9/5 + 32
    return celsius, fahrenheit

def mps_to_mph(mps):
    mph = mps * 2.23694
    return mph

def get_weather_data(city):
    url = BASE_URL + "appid=" + weather_config.api_key + "&q=" + city
    response = requests.get(url).json()
    return response

def get_timezone_name(offset):
    offset_hours = offset / 3600
    if offset_hours > 0:
        return f"Etc/GMT-{offset_hours:.0f}"
    elif offset_hours < 0:
        return f"Etc/GMT+{-offset_hours:.0f}"
    else:
        return "Etc/GMT"

def convert_to_local_time(utc_time, timezone_offset):
    utc_time = dt.datetime.utcfromtimestamp(utc_time)
    timezone_name = get_timezone_name(timezone_offset)
    local_tz = pytz.timezone(timezone_name)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_time

def get_temperature_unit():
    while True:
        choice = input("Do you want the temperature in Celsius or Fahrenheit? (C/F): ")
        if choice.lower() == "c":
            return "Celsius"
        elif choice.lower() == "f":
            return "Fahrenheit"
        else:
            print("Invalid choice. Please enter 'C' for Celsius or 'F' for Fahrenheit.")

def print_weather_info(city, temperature_celsius, temperature_fahrenheit, feels_like_celsius, feels_like_fahrenheit, humidity, wind_speed_mph, description, sunrise_time, sunset_time, response, time_format_choice, temperature_unit):
    print(f"Weather information for {city}:")
    if temperature_unit == "Celsius":
        print(f"Temperature: {temperature_celsius:.2f}°C")
        print(f"Feels like: {feels_like_celsius:.2f}°C")
    else:
        print(f"Temperature: {temperature_fahrenheit:.2f}°F")
        print(f"Feels like: {feels_like_fahrenheit:.2f}°F")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed_mph:.2f} mph")
    print(f"General Weather: {description}")

    if time_format_choice.lower() == "yes":
        sunrise_format = "%H:%M:%S"
        sunset_format = "%H:%M:%S"
    else:
        sunrise_format = "%I:%M:%S %p"
        sunset_format = "%I:%M:%S %p"

    sunrise_local_time = convert_to_local_time(sunrise_time, response['timezone'])
    sunset_local_time = convert_to_local_time(sunset_time, response['timezone'])

    print(f"Sunrise: {sunrise_local_time.strftime(sunrise_format)} local time.")
    print(f"Sunset: {sunset_local_time.strftime(sunset_format)} local time.")

def main():
    clear_screen()
    city = input("What city do you want the weather for? ")
    temperature_unit = get_temperature_unit()

    time_format_choice = input("Do you want the time in 24-hour format? (yes/no): ")

    clear_screen()
    response = get_weather_data(city)

    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)

    wind_speed_mps = response['wind']['speed']
    wind_speed_mph = mps_to_mph(wind_speed_mps)

    humidity = response['main']['humidity']
    description = response['weather'][0]['description']

    sunrise_time = response['sys']['sunrise'] + response['timezone']
    sunset_time = response['sys']['sunset'] + response['timezone']

    print_weather_info(city, temp_celsius, temp_fahrenheit, feels_like_celsius, feels_like_fahrenheit, humidity, wind_speed_mph, description, sunrise_time, sunset_time, response, time_format_choice, temperature_unit)

if __name__ == "__main__":
    main()

