import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)

# TODO: replace with your connection string.
logger.addHandler(AzureLogHandler(
    connection_string='')
)
# You can also instantiate the exporter directly if you have the environment variable
# `APPLICATIONINSIGHTS_CONNECTION_STRING` configured
# logger.addHandler(AzureLogHandler())


def value_prompt() -> bool:
    line = input("Enter a value (0 to exit): ")
    logger.warning(line)
    return line != "0"


def main():
    try:
        while value_prompt():
            logger.info("Hello World!")
            continue
    except Exception as e:
        logger.exception(f"Exception occurred: {e}")

    logger.warning("Exiting...")


if __name__ == "__main__":
    main()
