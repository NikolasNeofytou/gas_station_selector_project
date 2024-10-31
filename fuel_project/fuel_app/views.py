import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View


def index(request):
    return render(request, "fuel_app/index.html")


@csrf_exempt
def get_cities(request):
    try:
        api_url = "https://api.example.com/get-cities"  

        print("Attempting to fetch city data from external API...")

        response = requests.get(api_url)
        response.raise_for_status() 

        print("External API response:", response.text)

     
        data = response.json()

    
        if "cities" not in data:
            print("Unexpected data structure:", data)
            return JsonResponse(
                {"error": "Unexpected data structure from API"}, status=500
            )

        return JsonResponse(data, status=200)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return JsonResponse({"error": "HTTP error fetching city data"}, status=500)
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return JsonResponse(
            {"error": "Connection error fetching city data"}, status=500
        )
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return JsonResponse({"error": "Timeout error fetching city data"}, status=500)
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return JsonResponse({"error": "Request error fetching city data"}, status=500)
    except ValueError as json_err:
        print(f"JSON decode error occurred: {json_err}")
        return JsonResponse(
            {"error": "Failed to decode JSON from API response"}, status=500
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)


class FetchFuelPricesView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            city = data.get("city")
            fuel_type = data.get("fuel_type")

            api_url = "https://api.example.com/get-prices"

            payload = {
                "city": city,
                "fuel_type": fuel_type,
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer YOUR_API_KEY",
            }

            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            return JsonResponse({"data": response.json()}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"Error fetching data: {str(e)}"}, status=500)


@csrf_exempt
def proxy_polling_endpoint(request):
    try:
        data = json.loads(request.body)
        poll_url = data.get("pollUrl")

        if not poll_url:
            return JsonResponse({"error": "No pollUrl provided"}, status=400)

        headers = {
            "Content-Type": "application/xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        }

        response = requests.get(poll_url, headers=headers)
        response.raise_for_status()

        return JsonResponse({"data": response.text}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Failed to parse JSON request body"}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": f"Failed to fetch data from external API: {str(e)}"}, status=500
        )


def submit_fuel_request(request):
    if request.method == "POST":
        try:
            payload = {
            }

            headers = {
                "Content-Type": "application/xml",  # or 'application/json' if applicable
            }

            api_url = "https://aztest.cyprus.gov.cy/gg/submission"

            response = requests.post(api_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()  

            return JsonResponse(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Error during submission request: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def poll_fuel_data(request):
    if request.method == "POST":
        try:
            poll_url = "https://aztest.cyprus.gov.cy/gg/poll"

            response = requests.post(poll_url)
            response.raise_for_status()

            return JsonResponse(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Error during polling request: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
