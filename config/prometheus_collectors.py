from prometheus_client import Summary

SEND_MESSAGE_TIME = Summary("send_message_time", "Time spent sending message")
PROCESS_ORDERBOOK_TIME = Summary(
    "process_orderbook_time", "Time spent to process orderbook"
)
CALCULATE_DEVIATION_TIME = Summary(
    "calculate_deviation_time", "Time spent to calculate deviation"
)
