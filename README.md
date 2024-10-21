# Slack Message Dispatcher

**Slack Message Dispatcher** is a Python-based tool that listens to a specific Slack channel, evaluates messages based on predefined rules (keywords or regex), and forwards the messages to the appropriate target channels based on the configuration.

## Features

- **Real-Time Listening**: The bot listens for new messages in the source channel.
- **Message Dispatching**: Based on configurable rules, messages are routed to target channels.
- **Debug Mode**: Test message routing logic without dispatching messages.
- **Background Service**: Run as a daemon (background service) on Linux for continuous operation.

## Requirements

- **Python**: 3.7+
- **Slack SDK**: To interact with Slack's API.

### Install Dependencies

You can install the required dependencies using `pip`:

```bash
pip install slack_sdk
```

## Configuration

The tool relies on a `config.json` file for specifying Slack API credentials and rules for message dispatching.

### Example `config.json`

Here’s an example configuration file (`config.json`) with mock data:

```json
{
    "slack_bot_token": "xoxb-your-mock-slack-bot-token",
    "source_channel": "C01MOCKCHANNEL",
    "rules": [
        {
            "conditions": [
                {"keyword": "example1"}
            ],
            "target_channels": ["C02MOCKCHANNEL1"]
        },
        {
            "conditions": [
                {"keyword": "example2"}
            ],
            "target_channels": ["C02MOCKCHANNEL2"]
        },
        {
            "regex": "\\b(mock1|mock2|mock3|mockcorp|examplecorp|samplecorp)\\b",
            "target_channels": ["C03MOCKCHANNEL"]
        },
        {
            "regex": "(mockcountry)",
            "target_channels": ["C04MOCKCHANNEL"]
        },
        {
            "regex": "(mockregion)",
            "target_channels": ["C05MOCKCHANNEL"]
        }
    ]
}
```

### Explanation of `config.json`:

- **slack_bot_token**: The token for your Slack bot (mock data in this example).
- **source_channel**: The Slack channel ID where the bot will listen for messages.
- **rules**: A list of rules for dispatching messages based on conditions:
    - **conditions**: Simple keyword matching.
    - **regex**: Regular expression matching for more complex patterns.
- **target_channels**: A list of Slack channel IDs where matching messages will be forwarded.

## Usage

### Running the Tool

1. **Clone the Repository**:

```bash
git clone https://github.com/Arikius/slack-message-dispatcher.git
cd slack-message-dispatcher
```

2. **Install Dependencies**:

```bash
pip install slack_sdk
```

3. **Run the Tool**:

To run in **real-time listening mode**:

```bash
python slack_dispatcher.py
```

To run in **debug mode** (prints messages and shows which rule would match):

```bash
python slack_dispatcher.py --debug
```

## Running as a Background Service on Linux

You can set up the Slack Message Dispatcher to run as a service on Linux, so it continues to run even after logging out or rebooting the system. This can be achieved by creating a **systemd** service.

### Step-by-Step Instructions:

1. **Create a Service File**:

First, create a new service file under `/etc/systemd/system/` called `slack_dispatcher.service`:

```bash
sudo nano /etc/systemd/system/slack_dispatcher.service
```

2. **Define the Service Configuration**:

Add the following content to the service file:

```ini
[Unit]
Description=Slack Message Dispatcher
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/slack_dispatcher.py
WorkingDirectory=/path/to/your/project
StandardOutput=inherit
StandardError=inherit
Restart=always
User=your_linux_user

[Install]
WantedBy=multi-user.target
```

- **ExecStart**: The full path to the Python interpreter and the `slack_dispatcher.py` script.
- **WorkingDirectory**: The path to the directory where your project is located.
- **User**: The Linux user that will run the service.

3. **Reload systemd** to recognize the new service:

```bash
sudo systemctl daemon-reload
```

4. **Start the Service**:

```bash
sudo systemctl start slack_dispatcher.service
```

5. **Enable the Service** (so it starts on boot):

```bash
sudo systemctl enable slack_dispatcher.service
```

6. **Check the Status of the Service**:

To see if the service is running correctly:

```bash
sudo systemctl status slack_dispatcher.service
```

If the service is running properly, it will start automatically in the background each time the system boots up.

## Contributing

Feel free to open issues or contribute by submitting pull requests!

---

This `README.md` includes all the necessary information to set up, run, and deploy the Slack Message Dispatcher as a background service. Let me know if you need further modifications!
