import argparse
import logging
import json
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters


# logging
logging.basicConfig(level=logging.INFO)

# CLI arguments
parser = argparse.ArgumentParser(description='LinkedIn Job Scraper')
parser.add_argument('--query', type=str, required=True,
                    help='Job title to search for')
parser.add_argument('--location', type=str, nargs='+', required=True,
                    help='Job location(s), space-separated if multiple')
parser.add_argument('--limit', type=int, default=5,
                    help='Number of job postings to scrape')
parser.add_argument('--output', type=str,
                    default='linkedin_jobs.json', help='Output JSON file name')

args = parser.parse_args()

# results
job_results = []


def on_data(data: EventData):
    job = {
        'title': data.title,
        'company': data.company,
        'company_link': data.company_link,
        'company_img_link': data.company_img_link,
        'place': data.place,
        'date': data.date,
        'date_text': data.date_text,
        'link': data.link,
        'insights': data.insights,
        'apply_link': data.apply_link,
        'description': data.description
    }
    job_results.append(job)
    print('[ON_DATA]', job['title'], job['company'])


def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(job_results, f, ensure_ascii=False, indent=4)
    print(f'{len(job_results)} jobs saved to {args.output}')


scraper = LinkedinScraper(
    chrome_executable_path=None,
    chrome_binary_location=None,
    chrome_options=None,
    headless=True,
    max_workers=1,
    slow_mo=0.5,
    page_load_timeout=40
)

scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        query=args.query,
        options=QueryOptions(
            locations=args.location,
            apply_link=True,
            skip_promoted_jobs=True,
            page_offset=0,
            limit=args.limit,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
            )
        )
    ),
]

scraper.run(queries)
