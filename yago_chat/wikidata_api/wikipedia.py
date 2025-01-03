from typing import Optional

import aiohttp
import html2text

from bs4 import BeautifulSoup, Tag


async def _get_beautiful_soup(
        url: str, selector: str, selector_attrs: Optional[str] = None
) -> Tag:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            content = await response.text()

    soup = BeautifulSoup(content, 'html.parser')
    if selector_attrs:
        body = soup.find(selector, class_=selector_attrs) or soup.find('body')
    else:
        body = soup.find(selector) or soup.find('body')

    if body is None:
        raise ValueError("No matching element found.")

    return body


async def get_wikipedia_page_markdown(url, selector: str = "div", selector_attrs: str = "mw-body-content"):
    body = await _get_beautiful_soup(url,selector, selector_attrs)

    for tag in body.find_all(True):
        tag.attrs = {key: value for key, value in tag.attrs.items() if key == 'href'}

    html_content = str(body)
    markdown_converter = html2text.HTML2Text()
    markdown_converter.ignore_links = False
    markdown_converter.ignore_images = True
    markdown_converter.body_width = 0

    markdown_output = markdown_converter.handle(html_content)

    return markdown_output

