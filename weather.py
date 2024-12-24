import streamlit as st
import requests
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.trace.propagation import set_span_in_context

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
exporter = ConsoleSpanExporter()
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Set up the Streamlit app
st.title("Weather App")
st.subheader("Get the current weather for your city")

# Input for city name
city = st.text_input("Enter city name:", "")

# OpenWeatherMap API details
API_KEY = "<OPENWEATHER MAP API>"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

if city:
    logger.info(f"Received city input: {city}")
    trace_provider = trace.get_tracer_provider()
    with trace_provider.get_tracer(__name__).start_as_current_span("weather_trace", context=set_span_in_context(None)) as span:
        span.set_attribute("app.city", city)
        try:
            # API request
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'  # For temperature in Celsius
            }
            logger.info(f"Making API request to {BASE_URL} with params: {params}")
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            logger.info(f"API response received: {data}")

            if response.status_code == 200:
                # Extract relevant weather data
                weather = data["weather"][0]["description"].capitalize()
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                # Log weather details
                logger.info(f"Weather details - Condition: {weather}, Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s")
                span.set_attribute("weather.condition", weather)
                span.set_attribute("weather.temperature", temperature)
                span.set_attribute("weather.humidity", humidity)
                span.set_attribute("weather.wind_speed", wind_speed)

                # Display the weather information
                st.write(f"### Weather in {city.capitalize()}")
                st.write(f"- **Condition**: {weather}")
                st.write(f"- **Temperature**: {temperature} °C")
                st.write(f"- **Humidity**: {humidity}%")
                st.write(f"- **Wind Speed**: {wind_speed} m/s")
            else:
                logger.error(f"Failed to fetch weather for city {city}. Response code: {response.status_code}")
                span.set_attribute("error", True)
                st.error("City not found. Please check the city name and try again.")
        except Exception as e:
            logger.exception("An error occurred while fetching the weather data:")
            span.set_attribute("error", True)
            span.set_attribute("exception.message", str(e))
            st.error("An error occurred. Please try again later.")

# Run the app using: streamlit run app_name.py
