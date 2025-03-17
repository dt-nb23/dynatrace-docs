import os
import requests
from bs4 import BeautifulSoup
import markdownify
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_sitemap(sitemap_xml):
    soup = BeautifulSoup(sitemap_xml, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

def fetch_page(url, retries=5):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        if retries > 0:
            print(f"Error fetching {url} : {e}. Retrying...")
            time.sleep(5)
            return fetch_page(url, retries - 1)
        else:
            print(f"Failed to fetch {url} after multiple attempts.")
            raise

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Remove unwanted sections
    for section in soup.find_all(['header', 'footer', 'nav', 'aside']):
        section.decompose()
    # Extract main content
    main_content = soup.find('main') or soup.body
    return str(main_content)

def convert_to_markdown(html):
    return markdownify.markdownify(html, heading_style="ATX")

def save_markdown(content, filename, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    link = filename.replace('_', '/')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
        file.write(f"[Link to Documentation Page]({link})\n\n")

def process_url(url, output_dir):
    html = fetch_page(url)
    content = extract_content(html)
    markdown = convert_to_markdown(content)
    filename = url.replace('/', '_').replace(':', '') + '.md'
    save_markdown(markdown, filename, output_dir)
    return filename

def process_sitemap(sitemap_url, output_dir):
    sitemap_xml = fetch_sitemap(sitemap_url)
    urls = parse_sitemap(sitemap_xml)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_url, url, output_dir): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                filename = future.result()
                print(f'Saved {filename} in {output_dir}')
            except Exception as e:
                print(f'Error processing {url}: {e}')
            time.sleep(1)  # Add delay between requests

def main():
    sitemaps = {
        'https://docs.dynatrace.com/docs/sitemap.xml': 'dynatrace_saas',
        'https://docs.dynatrace.com/managed/sitemap.xml': 'dynatrace_managed'
    }
    
    for sitemap_url, output_dir in sitemaps.items():
        process_sitemap(sitemap_url, os.path.join('../outputs', output_dir))

if __name__ == "__main__":
    main()
