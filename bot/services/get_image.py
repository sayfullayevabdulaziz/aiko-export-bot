import aiohttp
from bs4 import BeautifulSoup
# from bot.utils.singleton import SingletonAikoMeta


class AikoClient:
        
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.session = None
            self.base_url = "https://aiko.uz/search/?query="
            self.initialized = True

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def fetch(self, code):
        async with self.session.get(f"{self.base_url}{code}") as response:
            return await response.text()

    async def fetch_image_url(self, code):
        html = await self.fetch(code)
        soup = BeautifulSoup(html, 'html.parser')
        # Find the div with class 'products__item-img' and then find the img tag within it
        # img_tag = soup.find('div', class_='products__item-img').find('img')
        span_tag = soup.find('div', class_='products__item-img').find('span', class_='products__img products__img_active')
        img_tag = span_tag.find('img')

        if img_tag and 'data-srcset' in img_tag.attrs:
            img_url = img_tag['data-srcset']
            img_url = img_url.split(',')[1]
            return img_url[:-3]
        else:
            raise ValueError('No image found at the provided URL')
        
    async def extract_prices(self, code):
        html = await self.fetch(code)
        soup = BeautifulSoup(html, 'html.parser')
        
        old_price_tag = soup.find("span", class_="compare-at-price nowrap")
        old_price = old_price_tag.get_text(strip=True) if old_price_tag else None

        available_price_tag = soup.select_one('.products__addtocart')
        available_price = None
        if available_price_tag:
            text_nodes = available_price_tag.find_all(string=True, recursive=False)
            for text in text_nodes:
                stripped_text = text.strip()
                if stripped_text and 'sum' in stripped_text:
                    available_price = stripped_text
                    break
        
        return available_price if old_price else None


    async def download_image(self, img_url, save_path):
        async with self.session.get(img_url) as response:
            with open(save_path, 'wb') as f:
                f.write(await response.read())


    async def extract_href(self, code):
        html = await self.fetch(code)
        soup = BeautifulSoup(html, 'html.parser')

        product_item = soup.select_one('.products__item a[href]')
        href = product_item['href'] if product_item else None
        return href