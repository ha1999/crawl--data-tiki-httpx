import asyncio
import re
import uuid
import httpx



async def crawl_data_by_page(client, page: int, q: str):
    try:
        url = 'https://tiki.vn/api/v2/products'
        params = {
            "limit": 40,
            # "include": "advertisement",
            # "aggregations": 2,
            "trackity_id": uuid.uuid4(),
            "q": q,
            "page": page
        }
        res = await client.get(url, params=params)
        if res.status_code > 200:
            return None
        json_data = res.json()
        return json_data["data"]
    except Exception as ex:
        print("Error: ", str(ex), " at page ", page)
        return []


async def main(q):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://tiki.vn/search?q={q}')
            match_html_limited_page = re.search('<span class="last">(\d+)</span>', response.text)
            limited_page = int(match_html_limited_page.groups(0)[0])
            res = await asyncio.gather(*[crawl_data_by_page(client, page, q) for page in range(1, limited_page + 1)])
            print(len(res))
    except Exception as ex:
        print(f"Error: {str(ex)}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main('điện+thoại'))
