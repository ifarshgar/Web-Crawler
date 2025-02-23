
# Website Asset Downloader

This Python script is a web crawler designed to download all assets from a specified website, enabling you to run the site locally and independently.

## Description

This tool automates the process of retrieving all static assets (images, stylesheets, scripts, fonts, etc.) from a given website. It recursively explores the website's structure, identifying and downloading all linked resources. This allows you to create a local copy of the website, which can be useful for:

* **Offline browsing:** Accessing website content without an internet connection.
* **Archiving:** Creating a local backup of a website.
* **Development:** Analyzing and modifying website assets for development or testing purposes.
* **Educational purposes:** learning how websites are structured.

## Features

* Recursive crawling of website links.
* Downloading of various asset types (images, CSS, JavaScript, fonts, etc.).
* Organized local storage of downloaded assets.
* Easy to use command line interface.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:ifarshgar/Web-Crawler.git
    cd Web-Crawler
    ```

2.  **Install dependencies:**

    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

To download assets from a website, run the following command:

```bash
python crawler.py 
