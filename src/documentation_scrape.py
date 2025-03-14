import os
import requests
from bs4 import BeautifulSoup
import markdownify
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_sitemap(sitemap_xml):
    soup = BeautifulSoup(sitemap_xml, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for section in soup.find_all('section'):
        section.decompose()
    return soup.get_text()

def convert_to_markdown(text):
    return markdownify.markdownify(text, heading_style="ATX")

def save_markdown(content, filename):
    output_dir = './outputs'
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def process_url(url):
    html = fetch_page(url)
    text = extract_content(html)
    markdown = convert_to_markdown(text)
    filename = url.split('/')[-1] + '.md'
    save_markdown(markdown, filename)
    return filename

def main(sitemap_url):
    sitemap_xml = fetch_sitemap(sitemap_url)
    urls = parse_sitemap(sitemap_xml)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_url, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                filename = future.result()
                print(f'Saved {filename}')
            except Exception as e:
                print(f'Error processing {url}: {e}')

if __name__ == "__main__":
    sitemap_url = 'https://docs.dynatrace.com/docs/sitemap.xml'
    main(sitemap_url)