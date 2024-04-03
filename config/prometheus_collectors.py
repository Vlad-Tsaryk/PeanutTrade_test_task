from prometheus_client import Summary

PROCESS_ORDERBOOK_TIME = Summary(
    "process_orderbook_time", "Time spent to process orderbook"
)
CALCULATE_DEVIATION_TIME = Summary(
    "calculate_deviation_time", "Time spent to calculate deviation"
)
