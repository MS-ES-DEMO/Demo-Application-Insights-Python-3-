import logging
from datetime import datetime

from opencensus.ext.azure import metrics_exporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

prompt_measure = measure_module.MeasureInt("prompts",
                                           "number of prompts",
                                           "prompts")
prompt_view = view_module.View("prompt view",
                               "number of prompts",
                               [],
                               prompt_measure,
                               aggregation_module.CountAggregation())
view_manager.register_view(prompt_view)
mmap = stats_recorder.new_measurement_map()
tmap = tag_map_module.TagMap()

logger = logging.getLogger(__name__)
connection_string: str = ""

logger.addHandler(AzureLogHandler(
    connection_string=connection_string)
)
# You can also instantiate the exporter directly if you have the environment variable
# `APPLICATIONINSIGHTS_CONNECTION_STRING` configured
# logger.addHandler(AzureLogHandler())

exporter = metrics_exporter.new_metrics_exporter(
    connection_string=connection_string)
# You can also instantiate the exporter directly if you have the environment variable
# `APPLICATIONINSIGHTS_CONNECTION_STRING` configured
# exporter = metrics_exporter.new_metrics_exporter()

view_manager.register_exporter(exporter)


def metrics_prompt():
    input("Press enter.")
    mmap.measure_int_put(prompt_measure, 1)
    mmap.record(tmap)
    metrics = list(mmap.measure_to_view_map.get_metrics(datetime.utcnow()))
    print(metrics[0].time_series[0].points[0])


def value_prompt() -> bool:
    line = input("Enter a value (0 to exit): ")
    logger.warning(line)
    return line != "0"


def main():
    logger.setLevel(logging.INFO)
    logger.info('Hello, this is a test Python app for App Insights')
    try:
        while value_prompt():
            logger.info("Hello World!")
            continue
    except Exception as e:
        logger.exception(f"Exception occurred: {e}")

    try:
        result = 1 / 0  # generate a ZeroDivisionError
    except ZeroDivisionError as e:
        logger.exception(f'Captured an exception. {e}')

    try:
        while True:
            metrics_prompt()
    except Exception as e:
        logger.exception(f"Exception occurred: {e}")
        logger.warning("Exiting the program...")


if __name__ == "__main__":
    main()
