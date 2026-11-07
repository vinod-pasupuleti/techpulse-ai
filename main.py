
import ssl
import certifi
import feedparser

from urllib.request import Request, urlopen

RSS_URLS: list[str] = [
    "https://blog.google/technology/ai/rss/",
    "https://openai.com/news/rss.xml",
    "https://deepmind.google/blog/rss.xml",
    "https://aws.amazon.com/blogs/machine-learning/feed/",
    "https://huggingface.co/blog/feed.xml"
]


def parse_rss_feed(rss_url: str):
    try:
        request = Request(
            rss_url,
            headers={"User-Agent": "TechPulseAI/0.1"}
        )

        context = ssl.create_default_context(
            cafile=certifi.where()
        )

        with urlopen(request, context=context, timeout=20) as response:
            content = response.read()
            return feedparser.parse(content)
    except Exception as e:
        print(f"Error fetching {rss_url}: {e}")
        return None


def collect_news(rss_urls: list[str]) -> list[dict]:
    articles = []
    seen_links = set()
    total = 0
    invalid_count = 0
    duplicate_count = 0


    for rss_url in rss_urls:
        try:
            feed = parse_rss_feed(rss_url)
            total += len(feed.entries)
            
            if feed is None:
                continue

            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()

                # Validate required fields
                if not title or not link:
                    invalid_count += 1
                    continue

                if link in seen_links:
                    duplicate_count += 1
                    continue
                
                seen_links.add(link)

                articles.append({
                    "title": title,
                    "link": link,
                    "published": entry.get("published"),
                    "source": feed.feed.get("title", "Unknown")
                })

            print(
                f"Source: {feed.feed.get('title', 'Unknown')} "
                f"| Articles: {len(feed.entries)}"
            )
        except Exception as e:
            print(f"Error fetching {rss_url}: {e}")
            continue
    print(f"Total RSS entries: {total}")
    print(f"Invalid articles: {invalid_count}")
    print(f"Duplicate articles: {duplicate_count}")
    print(f"Unique articles collected: {len(articles)}")

    return articles


if __name__ == "__main__":
    articles = collect_news(RSS_URLS)

    print(f"\nTotal articles collected: {len(articles)}")

    for article in articles[:5]:
        print(article)
