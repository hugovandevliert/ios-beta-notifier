# iOS Beta Notifier

This tool notifies you when one of your iOS beta applications become available!

This application periodically crawls iOS beta sites to determine its beta status.
When a beta status is changed to _open_, the Telegram bot notifies the user with a message.
Every day at 09:00, the user gets an overview of all betas.

## Installation

```bash
# clone the repo
git clone https://github.com/hugovandevliert/ios-beta-notifier

# change the working directory to ios-beta-notifier
cd ios-beta-notifier

# install python3 and python3-pip if they are not installed

# install the requirements
python3 -m pip install -r requirements.txt
```

## Setup

Make a copy of the `config.ini.example` file and save it as `config.ini`.
[Create a Telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and fill in the bot_token and chat_id properties.

### Adding betas

The `betas.yaml` file is used to specify what websites will be crawled.
To add a new beta, paste the following at the end of the `betas.yaml` file:

```yaml
-
    name: "BetaName"
    url: "https://testflight.apple.com/join/BetaUrl"
```

## Usage

To run the beta notifier:

```bash
python3 notifier.py
```

It is recommended to run the application as a background process or a service.

## Authors

Made by [@hugovandevliert](https://github.com/hugovandevliert).

## License

[![MIT](https://img.shields.io/cocoapods/l/AFNetworking.svg?style=style&label=License&maxAge=2592000)](LICENSE)

This software is distributed under the MIT license.
