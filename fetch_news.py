""""
Referencias:
- https://github.com/ranahaani/GNews/blob/master/README.md
- https://github.com/SSujitX/google-news-url-decoder
"""

import requests
import datetime
import pandas as pd
import time
from dateutil.relativedelta import relativedelta
from gnews import GNews
from googlenewsdecoder import new_decoderv1
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse


class News:
    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date = start_date
        self.end_date = end_date
        self.google_news = GNews(language='es', country='Argentina', start_date=start_date, end_date=end_date)

    def get_google_news(self, site):
        """Fetch news articles for the specified site and date range."""
        results = self.google_news.get_news_by_site(site)
        return results

    def update_google_news_dates(self, start_date, end_date):
        """Updates the google_news object with new start_date and end_date."""
        self.google_news.start_date = start_date
        self.google_news.end_date = end_date

    def get_article_content(self, article, time_interval=5):
        url = article['url']
        try:
            # Decode the Google News URL
            decoded_data = new_decoderv1(url, interval=time_interval)
            if decoded_data.get("status"):
                decoded_url = decoded_data["decoded_url"]
                response = requests.get(decoded_url)

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the HTML content
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract the description
                    description_tag = soup.find('meta', property='og:description')
                    description = description_tag.get('content') if description_tag else "Description not found."

                    # Extract article text
                    text = self.google_news.get_full_article(decoded_url).text

                    # Update article dictionary with description, text and url
                    article['url'] = decoded_url
                    article['description'] = description
                    article['text'] = text
                    return article
                else:
                    return {"error": f"Failed to retrieve the article from the decoded URL. Status code: {response.status_code}"}
            else:
                return {"error": f"Error decoding URL: {decoded_data['message']}"}
        except Exception as e:
            return {"error": str(e)}

    def fetch_articles(self, sites, time_interval=1):
        all_articles = []

        for site in sites:
            # Extract the domain or section name
            site_name = site.split('.com')[0].split('/')[-1]
            articles = self.get_google_news(site)

            for i in tqdm(range(len(articles)), desc=f"Processing articles from {site}"):
                article_content = self.get_article_content(articles[i], time_interval=time_interval)
                article_content['site'] = site_name
                all_articles.append(article_content)

        return all_articles


def main(output_file):
    # Sites to fetch articles from
    sites = ['lanacion.com.ar/economia', 'lanacion.com.ar/politica',
             'perfil.com/noticias/politica', 'perfil.com/noticias/economia',
             'clarin.com/economia', 'clarin.com/politica']

    news_fetcher = News(start_date=None, end_date=None)
    all_articles = []

    start = datetime.date(2022, 1, 1)
    end = datetime.date(2022, 6, 30)
    delta_days = 15

    # Fetch news for entire year increasing by delta_days
    while start <= end:
        current_end = min(start + datetime.timedelta(days=delta_days), end)
        news_fetcher.update_google_news_dates(start, current_end)

        print(f"Fetching articles starting at {start.strftime('%d %B %Y')}\n")

        articles = news_fetcher.fetch_articles(sites, time_interval=1)
        all_articles.extend(articles)

        start = start + datetime.timedelta(days=delta_days + 1)
        print('\n')
        time.sleep(5)

    # Save the data to a DataFrame
    articles_df = pd.DataFrame(all_articles)
    articles_df['id'] = articles_df.index + 1
    articles_df['text'] = articles_df['text'].str.replace('\n\n', '\n')

    # Save the DataFrame to a CSV file
    articles_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch news articles from specified sites.")
    parser.add_argument('--output_file', type=str, required=True, help="Path to output CSV file")

    args = parser.parse_args()

    main(args.output_file)
