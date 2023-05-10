import asyncio
import json
import re

import aiohttp
import cloudinary.uploader
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ImageUpload
from .serializers import ImageUploadSerializer


class ImageUploadListAPIView(generics.ListAPIView):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer


def get_public_id_from_url(image_url):
    pattern = r"/v(\d+)/[^/]+/([^/]+)$"
    match = re.search(pattern, image_url)
    if match:
        return match.group(2)
    return None


class UploadView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    @staticmethod
    def post(request):
        file = request.data.get("image")
        print("image", file)
        upload_data = cloudinary.uploader.upload(file)
        public_id = upload_data.get("public_id")
        user = request.user
        ImageUpload.objects.create(user=user, image=file, public_id=public_id)
        return Response(
            {
                "status": "success",
                "data": upload_data,
            },
            status=201,
        )


class BackgroundRemovalPrediction(APIView):
    def post(self, request, *args, **kwargs):
        url = "https://api.replicate.com/v1/predictions"
        headers = {
            "Authorization": f"Token {settings.REPLICATE_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "version": "fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003",
            "input": {"image": request.data.get("image")},
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code != 201:
            return JsonResponse({"detail": response.json().get("detail")}, status=500)

        return JsonResponse(response.json(), status=201)

    def get(self, request, *args, **kwargs):
        prediction_id = kwargs.get("id")
        url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        headers = {
            "Authorization": f"Token {settings.REPLICATE_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return JsonResponse({"detail": response.json().get("detail")}, status=500)

        return JsonResponse(response.json(), status=200, safe=False)


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


@api_view(["POST"])
def remove_background(request):
    public_id = request.data.get("public_id")

    if not public_id:
        return Response(
            {"error": "No public_id provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        response = cloudinary.uploader.explicit(
            public_id,
            transformation=[
                {"effect": "background_removal"},
                {"crop": "scale"},
                {"effect": "shadow:50", "x": 10, "y": 10},
            ],
            type="upload",
        )
        return Response({"result": response}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
