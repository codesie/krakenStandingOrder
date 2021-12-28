import json
import argparse
import os
import logging

from krakenConnector import KrakenRequests


def main(args, logger):
    """
    Main function of the script. Queries the current bid prices of the provided currencies and
    sends the order to the kraken api, if mode prod is provided.

    args (Namespace): contains the provided arguments. ex: Namespace(mode='debug')
    logger (logging): logging handler for writing to the log file
    """
    config_file = "/mnt/linuxData/01_Joel/02_Freizeit/Kryptowährungen/krakenStandingOrder/config.json"

    # initialize krakenConnector
    krqsts = KrakenRequests(config_file)

    # get standing order information from the config file
    standing_order_info = get_config(config_file)
    all_pairs = standing_order_info.keys()

    # Get current price information for provided pairs
    ticker_result = krqsts.get_kraken_data(all_pairs)
    logger.debug(json.dumps(ticker_result, indent=2))

    for pair in all_pairs:
        # last bid price
        price = float(ticker_result["result"][pair]["b"][0])
        # 24 h lowest price
        # price = float(ticker_result["result"][pair]["l"][1])
        volume = standing_order_info[pair] / price

        # Date for create order
        data = {
            "pair": pair,
            "type": "buy",
            "ordertype": "limit",
            "price": price,
            "volume": volume
        }

        if args.mode == "prod":
            logger.info("--- Order placed on kraken!")
            result = krqsts.create_order(data)
            if len(result["error"]) > 0:
                logger.error(result)
        else:
            logger.info(
                "--- No order placed on kraken! Shows the order which would have been executed in prod mode.")

        logger.info(json.dumps(data, indent=2))


def get_config(config_file):
    """
    Get the content of the config.json file, which includes the amount of euros to spend per trade, which
    currencies to trade and more.

    Returns:
    json:Content of the file
    """
    with open(config_file) as file:
        config_content = json.load(file)
    standing_order_info = config_content["standingOrder"]

    return standing_order_info


def initialize_logger():
    """
    Here a logger is initialized. It displays outputs in the console and logs them as well to
    a log file. Thereby we have a persistent history of our file execution.

    logging:the logger object
    """
    try:
        logger = logging.getLogger("kraken_crypto")
        logger.setLevel(logging.INFO)

        init_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        script_dir = os.path.dirname(__file__)
        log_file = os.path.join(script_dir, "..", "logs", "kraken_standing_order.log")
        init_handler = logging.FileHandler(log_file)
        init_handler.setFormatter(init_formatter)

        init_stream = logging.StreamHandler()
        init_stream.setLevel(logging.INFO)
        init_stream.setFormatter(init_formatter)

        logger.addHandler(init_handler)
        logger.addHandler(init_stream)
        return logger
    except Exception as e:
        print("logger.initial_setup\n"
              "- " + str(e))


if __name__ == "__main__":
    """
    Main entry of the script. First, the provided arguments are parsed and then the main purpose of the script is 
    executed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--mode", help="run the script in demo mode, without executing the order, or in production mode, which places an order.", default="demo")
    args = parser.parse_args()
    logger = initialize_logger()
    main(args, logger)
