# iOS Beta Crawler

A tool for checking iOS beta availability.

## Installation

```bash
# clone the repo
git clone https://github.com/hugovandevliert/ios-beta-crawler

# change the working directory to ios-beta-crawler
cd ios-beta-crawler

# install python3 and python3-pip if they are not installed

# install the requirements
python3 -m pip install -r requirements.txt
```

<!-- Disabled as long as this repo is private -->
<!-- [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.png)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/hugovandevliert/ios-beta-crawler&tutorial=README.md) -->

## Usage

To run the beta crawler:

```bash
python3 beta-crawler.py
```

The `betas.yaml` file is used to specify what websites will be crawled.
To add a new beta to crawl, paste the following at the end of the `betas.yaml` file:

```yaml
-
    name: "BetaName"
    url: "https://testflight.apple.com/join/BetaUrl"
```

## Authors

Made by @hugovandevliert.

## License

[![MIT](https://img.shields.io/cocoapods/l/AFNetworking.svg?style=style&label=License&maxAge=2592000)](LICENSE)

This software is distributed under the MIT license.
