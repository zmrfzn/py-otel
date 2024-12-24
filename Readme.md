
```bash
pip install opentelemetry-distro
opentelemetry-bootstrap -a install
```

## dry run locall export 

```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name weather-central \
    streamlit run weather.py
```

## export telemetry to NR
```bash
OTEL_SERVICE_NAME=weather-central \
OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp.nr-data.net:4317 \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
OTEL_EXPORTER_OTLP_HEADERS=api-key=***REMOVED*** \
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console \
    streamlit run weather.py
```    