# Documentation Scraper

This project is a Python script that fetches a sitemap, extracts content from the URLs listed in the sitemap, converts the content to Markdown format, and saves it to files. It utilizes several libraries, including `requests`, `BeautifulSoup`, and `markdownify`.

## Project Structure

```
documentation_scrape
├── src
│   └── documentation_scrape.py  # The main script for scraping and converting content
├── Dockerfile                     # Dockerfile to build the Docker image
├── requirements.txt               # Python dependencies
├── .github
│   └── workflows
│       └── main.yml              # GitHub Actions workflow for automation
└── README.md                     # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd documentation_scrape
   ```

2. **Install Dependencies**
   You can install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Script**
   To run the script, execute the following command:
   ```bash
   python src/documentation_scrape.py
   ```

## Docker Setup

To run the project in a Docker container, follow these steps:

1. **Build the Docker Image**
   ```bash
   docker build -t documentation_scraper .
   ```

2. **Run the Docker Container**
   ```bash
   docker run documentation_scraper
   ```

## GitHub Actions

The project includes a GitHub Actions workflow located in `.github/workflows/main.yml` that automates the process of running the script daily and pushing the results to the GitHub repository. 

## Functionality

- **Fetch Sitemap**: The script fetches the sitemap from a specified URL.
- **Extract Content**: It extracts content from each URL listed in the sitemap.
- **Convert to Markdown**: The extracted content is converted to Markdown format.
- **Save Files**: The Markdown files are saved in the `outputs` directory.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.