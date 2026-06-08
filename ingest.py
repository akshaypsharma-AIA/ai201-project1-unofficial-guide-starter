import requests
import json
import os
import time
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
DOCUMENTS_DIR = "documents"
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

REDDIT_THREADS = [
    "https://www.reddit.com/r/UofT/comments/n7h98q/help_others_by_submitting_a_review_for_all_your/",
    "https://www.reddit.com/r/UofT/comments/1tirtnu/any_suggestions_on_what_csc_300400_level_courses/",
    "https://www.reddit.com/r/UofT/comments/1ouc9zd/finding_professors_to_work_with_for_graduate/",
    "https://www.reddit.com/r/UofT/comments/11qau12/avoid_csc401_im_even_not_kidding/",
    "https://www.reddit.com/r/UofT/comments/1kjq8ji/rating_and_reviewing_every_course_i_took_at_uoft/",
    "https://www.reddit.com/r/UofT/comments/2u8ral/u_of_t_redditors_whos_the_best_instructor_you_had/",
    "https://www.reddit.com/r/UofT/comments/7kelyu/best_profs_for_csc148165/",
    "https://www.reddit.com/r/UofT/comments/4rdqw7/utsc_cs_1st_year_who_are_the_best_professors/",
    "https://www.reddit.com/r/UofT/comments/1ed0ww/comp_sci_first_year_at_utsg_best_profs_best/",
    "https://www.reddit.com/r/UofT/comments/1e0xd39/what_professors_are_the_best_at_utsg_for_math_and/",
]

RMP_URLS = [
    "https://www.ratemyprofessors.com/professor/1694041",
    "https://www.ratemyprofessors.com/professor/3121445",
    "https://www.ratemyprofessors.com/professor/2340488",
    "https://www.ratemyprofessors.com/professor/20260",
    "https://www.ratemyprofessors.com/professor/1443534",
    "https://www.ratemyprofessors.com/professor/3118690",
    "https://www.ratemyprofessors.com/professor/2127391",
    "https://www.ratemyprofessors.com/professor/30803",
    "https://www.ratemyprofessors.com/professor/30200",
    "https://www.ratemyprofessors.com/professor/69474",
    "https://www.ratemyprofessors.com/professor/3042719",
]

def scrape_reddit_thread(url):
    json_url = url.rstrip("/") + ".json"
    try:
        r = requests.get(json_url, headers=HEADERS, timeout=10)
        data = r.json()
        post = data[0]["data"]["children"][0]["data"]
        title = post["title"]
        body = post.get("selftext", "")
        comments = []
        for child in data[1]["data"]["children"]:
            comment = child["data"].get("body", "")
            if comment and comment != "[deleted]" and comment != "[removed]":
                # prepend thread title to every comment for context
                comments.append(f"Thread: {title}\n{comment}")
        full_text = f"Thread: {title}\n\n{body}\n\n" + "\n\n".join(comments)
        return title, full_text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None, None

def scrape_rmp(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # extract all visible text from review cards
        reviews = soup.find_all("div", {"class": lambda c: c and "Comments__StyledComments" in c})
        if not reviews:
            # fallback: grab all paragraph text
            reviews = soup.find_all("p")
        text = "\n\n".join([r.get_text(strip=True) for r in reviews if r.get_text(strip=True)])
        professor = soup.find("div", {"class": lambda c: c and "NameTitle" in c})
        name = professor.get_text(strip=True) if professor else url.split("/")[-1]
        return name, text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None, None

def ingest_all():
    print("--- Scraping Reddit threads ---")
    for i, url in enumerate(REDDIT_THREADS):
        title, text = scrape_reddit_thread(url)
        if text:
            filename = f"reddit_{i+1}.txt"
            with open(os.path.join(DOCUMENTS_DIR, filename), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved {filename} — {title[:60]}")
        time.sleep(1)

    print("\n--- Scraping Rate My Professors ---")
    for i, url in enumerate(RMP_URLS):
        name, text = scrape_rmp(url)
        if text:
            filename = f"rmp_{i+1}.txt"
            with open(os.path.join(DOCUMENTS_DIR, filename), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved {filename} — {name}")
        time.sleep(2)

    print("\nIngestion complete.")
    print(f"Files saved to /{DOCUMENTS_DIR}")

if __name__ == "__main__":
    ingest_all()