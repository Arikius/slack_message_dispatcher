import json
import re
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import argparse

# Load configuration from JSON
with open('config.json') as f:
    config = json.load(f)

client = WebClient(token=config['slack_bot_token'])

def check_rules(message_text):
    print(f"Evaluating message: {message_text}")

    for rule in config["rules"]:
        conditions_met = True

        if "conditions" in rule:
            for condition in rule["conditions"]:
                if "keyword" in condition:
                    if condition["keyword"].lower() not in message_text.lower():
                        conditions_met = False
                        break
                elif "regex" in condition:
                    if not re.search(condition["regex"], message_text, re.IGNORECASE):
                        conditions_met = False
                        break

        elif "regex" in rule:
            if not re.search(rule["regex"], message_text, re.IGNORECASE):
                conditions_met = False

        if conditions_met:
            print(f"Rule matched: {rule}, routing to: {rule.get('target_channels', [])}")
            return rule.get("target_channels", [])

        else:
            print(f"Rule did not match: {rule}")

    return None

def fetch_full_message(channel_id, timestamp):
    try:
        response = client.conversations_history(
            channel=channel_id,
            latest=timestamp,
            inclusive=True,
            limit=1
        )
        messages = response['messages']
        if messages:
            return messages[0]['text']
    except SlackApiError as e:
        print(f"Error fetching message: {e.response['error']}")
    return None

def dispatch_message(full_message, target_channels):
    for channel in target_channels:
        try:
            client.chat_postMessage(channel=channel, text=full_message)
        except SlackApiError as e:
            print(f"Error posting to {channel}: {e.response['error']}")

def listen_to_channel():
    last_timestamp = None
    while True:
        try:
            response = client.conversations_history(
                channel=config["source_channel"],
                oldest=last_timestamp,
                inclusive=False,
                limit=5
            )
            messages = response['messages']
            
            for message in reversed(messages):
                # Fetch the full message text without user or timestamp
                full_message = fetch_full_message(config["source_channel"], message['ts'])
                if full_message:
                    # Apply rule matching and dispatch the message if it matches any rule
                    target_channels = check_rules(full_message)
                    if target_channels:
                        dispatch_message(full_message, target_channels)
            
            if messages:
                last_timestamp = messages[0]['ts']
            
            time.sleep(1)
        except SlackApiError as e:
            print(f"Error fetching conversation history: {e.response['error']}")
            time.sleep(5)  # Wait a bit longer if there's an error

def debug_mode():
    five_minutes_ago = time.time() - 300
    try:
        response = client.conversations_history(
            channel=config["source_channel"],
            oldest=five_minutes_ago,
            inclusive=False,
            limit=100
        )
        messages = response.get('messages', [])

        print(f"Fetched {len(messages)} messages from the last 5 minutes.")

        for message in reversed(messages):
            full_message = fetch_full_message(config["source_channel"], message['ts'])
            print(f"Processing message: {full_message}")
            target_channels = check_rules(full_message)
            if target_channels:
                print(f"Message: '{full_message}' would be moved to {target_channels} - Rule hit")
            else:
                print(f"Message: '{full_message}' does not match any rule")
    except SlackApiError as e:
        print(f"Error fetching conversation history: {e.response['error']}")

def main():
    parser = argparse.ArgumentParser(description='Slack Dispatcher')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()

    if args.debug:
        debug_mode()
    else:
        listen_to_channel()

if __name__ == "__main__":
    main()
