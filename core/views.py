from rest_framework.response import Response
from rest_framework.views import APIView
from core import logger
from .models import URL

import string
import random

"""
An error occurred creating the short URL
The URL has not been shortened, possible errors:

Check if the domain is correct
Check if the site is online
Check the address bars and punctuation
The URL may be being used for spam
The URL may have been blocked
The URL may have been reported
The URL was recently shortened
The URL is not allowed
You shortened many URLs in a short time

# TODO: Add a check to ensure Local Host URLs are not shortened
"""


# this won't work need to go ahead with a hash function.
def short_random_string(n: int) -> str:
    return ''.join(
        random.SystemRandom(
        ).choice(string.ascii_letters + string.digits) for _ in range(n)
    )

class UrlShortenerView(APIView):
    def get(self, request, short_code):
        try:
            # Extract the short code from the request
            short_url = URL.objects.filter(short_code=short_code).first()
            if not short_url:
                return Response({"message": "URL not found"}, status=404)
            # send the actual url in the response
            return Response({
                    "redirect_url":short_url.original_url
                }
            ,status=200)
        except Exception as e:
            logger.info(f"Error occurred: {str(e)}")
            raise Exception(f"An error occurred: {str(e)}")

    def post(self, request):
        try:
            # Extract the URL from the request
            url = request.data.get("url")
            if not url:
                return Response({"error": "URL is required"}, status=400)

            short_code = short_random_string(6)
            short_url = URL.objects.create(
                original_url=url,
                short_code=short_code,  # This should be generated
            )
            # need to parse the input url and get the domain name
            domain = request.build_absolute_uri('/').split('/')[2]
            logger.info(f"Shortened URL: {domain}/{short_url.short_code}")
            return Response({"result": {
                "short_url": f"{request.META.get('HTTP_HOST')}/{short_url.short_code}",
                "original_url": short_url.original_url,
                "short_code": short_url.short_code
            }}, status=200)
        except Exception as e:
            logger.info(f"Error occurred: {str(e)}")
            raise Exception(f"An error occurred: {str(e)}")
