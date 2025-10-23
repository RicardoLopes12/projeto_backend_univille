import datetime
import logging

logging.basicConfig(level=logging.INFO)

def hello(name="World"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"👋 Hello, {name}! Time now: {now}"
    logging.info(message)
    return message

if __name__ == "__main__":
    hello()