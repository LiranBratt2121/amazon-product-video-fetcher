# core/extract_links.py
import re
import asyncio
from playwright.async_api import async_playwright

async def extract_m3u8_links(page_url: str, headless: bool = True) -> list[str]:
    """Fetch all .m3u8 links from a page, preserving order."""
    found_urls = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        async def on_response(response):
            try:
                if response.url.endswith(".m3u8") and response.url not in found_urls:
                    found_urls.append(response.url)
                else:
                    ct = response.headers.get("content-type", "")
                    if "json" in ct or "text" in ct:
                        text = await response.text()
                        matches = re.findall(r"https?://[^\s\"']+\.m3u8", text)
                        for url in matches:
                            if url not in found_urls:
                                found_urls.append(url)
            except Exception:
                pass

        page.on("response", on_response)
        await page.goto(page_url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)  # wait for all streams to load
        await browser.close()

    return found_urls

def get_m3u8_links(url: str) -> list[str]:
    return asyncio.run(extract_m3u8_links(url))
