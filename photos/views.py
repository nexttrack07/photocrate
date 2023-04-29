import asyncio

import aiohttp
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class PopularImages(APIView):
    async def fetch_images(self, session, url, headers):
        async with session.get(url, headers=headers) as response:
            return await response.json()

    async def get_popular_images(self):
        pexels_url = "https://api.pexels.com/v1/popular"
        # unsplash_url = 'https://api.unsplash.com/photos/popular'

        # Replace with your API keys
        pexels_headers = {"Authorization": settings.PEXELS_API_KEY}
        # unsplash_headers = {'Authorization': 'Client-ID Unsplash-API-Key'}

        async with aiohttp.ClientSession() as session:
            pexels_task = asyncio.create_task(
                self.fetch_images(session, pexels_url, pexels_headers)
            )
            # unsplash_task = asyncio.create_task(self.fetch_images(session, unsplash_url, unsplash_headers))
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

            # for image in unsplash_images:
            #     consolidated_images.append({
            #         'id': image['id'],
            #         'url': image['urls']['regular'],
            #         'source': 'Unsplash'
            #     })

            return consolidated_images

    def get(self, request):
        popular_images = asyncio.run(self.get_popular_images())
        return Response(popular_images)
