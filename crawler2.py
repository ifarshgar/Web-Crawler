import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

DOWNLOADS_FOLDER = 'Downloads'
visited_urls = set()  # Track visited URLs to avoid duplicates
MAX_DEPTH = 5  # Maximum depth for recursive crawling

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

    domain_parts = folder_name.split('.')
    if len(domain_parts) > 1:
        domain_parts[-1] = f'-{domain_parts[-1]}'
        folder_name = '.'.join(domain_parts)

    return folder_name

# Function to clean the path by removing unnecessary parent folders
def clean_path(path):
    # Split the path into parts
    parts = path.split('/')
    # Remove empty parts (e.g., from leading/trailing slashes)
    parts = [part for part in parts if part]
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
def download_assets(url, base_folder, depth=0):
    # Stop if the depth exceeds the maximum limit
    if depth > MAX_DEPTH:
        print(f"Reached maximum depth ({MAX_DEPTH}) for URL: {url}")
        return

    # Skip if the URL has already been visited
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Create the base folder if it doesn't exist
    os.makedirs(base_folder, exist_ok=True)

    # Save the HTML file
    html_file_name = os.path.basename(urlparse(url).path) or 'index.html'
    html_file_path = os.path.join(base_folder, html_file_name)
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Saved HTML: {html_file_path}")

    # Download CSS files
    for link in soup.find_all('link', href=True):
        if 'stylesheet' in link.get('rel', []):
            css_url = urljoin(url, link['href'])
            try:
                css_path = download_file(css_url, base_folder)
                # Parse the CSS file to find font files
                with open(css_path, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                # Find font URLs in the CSS file
                import re
                font_urls = re.findall(r'url\((.*?)\)', css_content)
                for font_url in font_urls:
                    font_url = font_url.strip('"\'').strip('"\'').strip()
                    if font_url.startswith('http'):
                        continue  # Skip absolute URLs
                    full_font_url = urljoin(css_url, font_url)
                    try:
                        download_file(full_font_url, base_folder)
                    except Exception as e:
                        print(f"Failed to download font {full_font_url}: {e}")
            except Exception as e:
                print(f"Failed to download {css_url}: {e}")

    # Download JavaScript files
    for script in soup.find_all('script', src=True):
        js_url = urljoin(url, script['src'])
        try:
            download_file(js_url, base_folder)
        except Exception as e:
            print(f"Failed to download {js_url}: {e}")

    # Download images
    for img in soup.find_all('img', src=True):
        img_url = urljoin(url, img['src'])
        try:
            download_file(img_url, base_folder)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

    # Download favicons
    for link in soup.find_all('link', rel=['icon', 'apple-touch-icon']):
        icon_url = urljoin(url, link['href'])
        try:
            download_file(icon_url, base_folder)
        except Exception as e:
            print(f"Failed to download {icon_url}: {e}")

    # Recursively download linked pages within the same domain
    for a in soup.find_all('a', href=True):
        linked_url = urljoin(url, a['href'])
        parsed_linked_url = urlparse(linked_url)
        if parsed_linked_url.netloc == urlparse(url).netloc:
            if linked_url not in visited_urls:  # Avoid circular links
                download_assets(linked_url, base_folder, depth + 1)  # Increment depth

# Example usage
url = input('Please enter your URL: ')
folder_name = create_unique_folder_name(url)
base_folder = os.path.join(DOWNLOADS_FOLDER, folder_name)

# Extract the base path from the URL (e.g., /html/pylon1/)
parsed_url = urlparse(url)
base_path = os.path.dirname(parsed_url.path).strip('/')
html_folder = os.path.join(base_folder, base_path)

# Create the HTML folder if it doesn't exist
os.makedirs(html_folder, exist_ok=True)

print('Your assets will be saved to: \n', base_folder)

download_assets(url, html_folder)
