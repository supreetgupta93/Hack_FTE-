# ================================
# 🏆 Hackathon Template Notebook
# Prospect Research Agent
# ================================


import json
import os
import re
import requests
import tldextract
import google.generativeai as genai

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
def fetch_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code == 200:
            return response.text

    except:
        pass

    return ""
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_text(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup(
        ["script", "style", "noscript"]
    ):
        tag.decompose()

    return clean_text(
        soup.get_text(" ")
    )


def extract_emails(text):

    return list(
        set(
            re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                text
            )
        )
    )


def extract_phone(text):

    phones = re.findall(
        r'(\+?\d[\d\s\-\(\)]{8,}\d)',
        text
    )

    return phones[0] if phones else ""


def get_links(base_url, html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = []

    for a in soup.find_all(
        "a",
        href=True
    ):
        links.append(
            urljoin(
                base_url,
                a["href"]
            )
        )

    return list(set(links))


def get_relevant_pages(links):

    keywords = [
        "about",
        "contact",
        "service",
        "solution",
        "company"
    ]

    pages = []

    for link in links:

        lower = link.lower()

        if any(
            k in lower
            for k in keywords
        ):
            pages.append(link)

    return pages[:10]


def ai_analysis(text):
    if not API_KEY or model is None:
        raise RuntimeError("GEMINI_API_KEY must be set to perform AI analysis")

    prompt = f"""
Using ONLY the website content below,
extract:

company_name
core_service
target_customer
probable_pain_point
outreach_opener

Rules:
- Return valid JSON only.
- Do not use markdown.
- If information is missing, use "".

CONTENT:
{text[:12000]}
"""

    response = model.generate_content(prompt)
    output = response.text.strip()
    output = output.replace("```json", "")
    output = output.replace("```", "")
    output = output.strip()
    return json.loads(output)




# ========= REQUIRED FUNCTION =========
def enrich_company(url: str) -> dict:
    """
    Input: Company URL
    Output: Structured company profile (STRICT FORMAT)
    """

    homepage = fetch_page(url)

    homepage_text = extract_text(
        homepage
    )

    emails = extract_emails(
        homepage
    )

    phone = extract_phone(
        homepage
    )

    links = get_links(
        url,
        homepage
    )

    pages = get_relevant_pages(
        links
    )

    all_text = homepage_text

    for page in pages:

        html = fetch_page(page)

        if html:

            all_text += "\n\n"
            all_text += extract_text(html)

            emails.extend(
                extract_emails(html)
            )

            if not phone:
                phone = extract_phone(html)

    emails = list(set(emails))

    ai_data = ai_analysis(
        all_text
    )

    website_name = (
        tldextract.extract(url)
        .domain
        .replace("-", " ")
        .title()
    )

    return {
        "website_name": website_name,
        "company_name": ai_data.get("company_name", ""),
        "address": "",
        "mobile_number": phone,
        "mail": emails,
        "core_service": ai_data.get("core_service", ""),
        "target_customer": ai_data.get("target_customer", ""),
        "probable_pain_point": ai_data.get("probable_pain_point", ""),
        "outreach_opener": ai_data.get("outreach_opener", "")
    }


