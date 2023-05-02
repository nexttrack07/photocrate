import asyncio

import aiohttp
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


async def fetch_images(session, url, headers, params):
    async with session.get(url, headers=headers, params=params) as response:
        return await response.json()


class PopularImages(APIView):
    async def get_popular_images(self, page_number=1):
        pexels_url = "https://api.pexels.com/v1/popular"
        pexels_headers = {"Authorization": settings.PEXELS_API_KEY}
        pexels_params = {"page": page_number, "per_page": 20}

        async with aiohttp.ClientSession() as session:
            pexels_task = asyncio.create_task(
                fetch_images(session, pexels_url, pexels_headers, pexels_params)
            )
            pexels_images = await asyncio.gather(pexels_task)

            # Process and consolidate the responses here
            consolidated_images = []
            for image in pexels_images[0]["photos"]:
                consolidated_images.append(
                    {
                        "id": image["id"],
                        "src": image["src"]["large"],
                        "source": "Pexels",
                        "url": image["url"],
                        "thumb": image["src"]["tiny"],
                        "alt": image["alt"],
                    }
                )

            return consolidated_images

    def get(self, request):
        page_number = request.query_params.get("page", 1)
        popular_images = asyncio.run(self.get_popular_images(page_number))
        return Response({"page": page_number, "images": popular_images})


class SearchImages(APIView):
    async def search_images(self, query, per_page=10, page_number=1):
        pexels_url = "https://api.pexels.com/v1/search"
        pexels_headers = {"Authorization": settings.PEXELS_API_KEY}
        pexels_params = {"query": query, "per_page": per_page, "page": page_number}

        async with aiohttp.ClientSession() as session:
            pexels_task = asyncio.create_task(
                fetch_images(session, pexels_url, pexels_headers, pexels_params)
            )
            pexels_images = await asyncio.gather(pexels_task)

            print("Pexels: ", pexels_images)

            # Process and consolidate the responses here
            consolidated_images = []
            for image in pexels_images[0]["photos"]:
                consolidated_images.append(
                    {
                        "id": image["id"],
                        "src": image["src"]["large"],
                        "source": "Pexels",
                        "url": image["url"],
                        "thumb": image["src"]["tiny"],
                        "alt": image["alt"],
                    }
                )

            return consolidated_images

    def get(self, request):
        query = request.query_params.get("query", "")
        page_number = request.query_params.get("page", 1)
        per_page = request.query_params.get("per_page", 20)
        search_images = asyncio.run(self.search_images(query, per_page, page_number))
        return Response({"page": page_number, "images": search_images})
