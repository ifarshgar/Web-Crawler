import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

DOWNLOADS_FOLDER = 'Downloads'

# Function to create a unique folder name based on the URL
def create_unique_folder_name(url):
    parsed_url = urlparse(url)
    base_folder_name = parsed_url.netloc  # Extract domain (e.g., webdevcode.com)
    folder_name = base_folder_name
    counter = 1

    # Check if the folder already exists and increment the counter if necessary
    while os.path.exists(os.path.join(DOWNLOADS_FOLDER, folder_name)):
        folder_name = f"{base_folder_name}{counter}"
        counter += 1

    return folder_name

# Function to clean the path by removing unnecessary parent folders
def clean_path(path):
    # Split the path into parts
    parts = path.split('/')
    # Remove unnecessary parent folders like 'html/pylon1/assets'
    if 'html' in parts and 'pylon1' in parts and 'assets' in parts:
        # Find the index of 'assets' and keep everything after it
        assets_index = parts.index('assets')
        parts = parts[assets_index + 1:]
    # Rejoin the parts into a clean path
    return '/'.join(parts)

# Function to download a file and preserve the cleaned directory structure
def download_file(url, base_folder):
    parsed_url = urlparse(url)
    # Extract the relative path (e.g., css/style.css, js/script.js, images/logo.png)
    relative_path = parsed_url.path.strip('/')
    # Clean the path to remove unnecessary parent folders
    cleaned_path = clean_path(relative_path)
    local_path = os.path.join(base_folder, cleaned_path)

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Download the file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {url} -> {local_path}")
    return local_path

# Function to download all assets and preserve the cleaned directory structure
def download_assets(url, base_folder):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create the base folder if it doesn't exist
    os.makedirs(base_folder, exist_ok=True)

    # Save the HTML file
    html_file_path = os.path.join(base_folder, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Saved HTML: {html_file_path}")

    # Create an assets folder alongside the index.html
    assets_folder = os.path.join(base_folder, 'assets')
    os.makedirs(assets_folder, exist_ok=True)

    # Download CSS files
    for link in soup.find_all('link', href=True):
        css_url = urljoin(url, link['href'])
        try:
            download_file(css_url, assets_folder)
        except Exception as e:
            print(f"Failed to download {css_url}: {e}")

    # Download JavaScript files
    for script in soup.find_all('script', src=True):
        js_url = urljoin(url, script['src'])
        try:
            download_file(js_url, assets_folder)
        except Exception as e:
            print(f"Failed to download {js_url}: {e}")

    # Download images
    for img in soup.find_all('img', src=True):
        img_url = urljoin(url, img['src'])
        try:
            download_file(img_url, assets_folder)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

    # Download favicons
    for link in soup.find_all('link', rel=['icon', 'apple-touch-icon']):
        icon_url = urljoin(url, link['href'])
        try:
            download_file(icon_url, assets_folder)
        except Exception as e:
            print(f"Failed to download {icon_url}: {e}")

# Example usage
url = input('Please enter your URL: ')
folder_name = create_unique_folder_name(url)
base_folder = os.path.join(DOWNLOADS_FOLDER, folder_name)
print('Your assets will be saved to: \n', base_folder)

download_assets(url, base_folder)
