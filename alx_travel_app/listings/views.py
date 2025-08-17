from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from .models import Payment

CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")
CHAPA_BASE_URL = "https://api.chapa.co/v1/transaction"

@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        # Extract details (you can replace with serializer if using DRF)
        data = request.POST
        amount = data.get("amount")
        booking_ref = data.get("booking_reference", get_random_string(10))

        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": data.get("email", "test@example.com"),
            "first_name": data.get("first_name", "John"),
            "last_name": data.get("last_name", "Doe"),
            "tx_ref": booking_ref,
            "callback_url": "http://localhost:8000/api/payments/verify/",
        }

        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}

        response = requests.post(f"{CHAPA_BASE_URL}/initialize", json=payload, headers=headers)

        if response.status_code == 200:
            res_data = response.json()
            transaction_id = res_data["data"]["tx_ref"]
            checkout_url = res_data["data"]["checkout_url"]

            # Save payment
            Payment.objects.create(
                booking_reference=booking_ref,
                transaction_id=transaction_id,
                amount=amount,
                status="Pending"
            )

            return JsonResponse({"checkout_url": checkout_url, "transaction_id": transaction_id})
        else:
            return JsonResponse({"error": response.json()}, status=400)


@csrf_exempt
def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")

    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    response = requests.get(f"{CHAPA_BASE_URL}/verify/{tx_ref}", headers=headers)

    if response.status_code == 200:
        res_data = response.json()
        status = res_data["data"]["status"]

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            if status == "success":
                payment.status = "Completed"
            else:
                payment.status = "Failed"
            payment.save()
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

        return JsonResponse({"status": payment.status})
    else:
        return JsonResponse({"error": response.json()}, status=400)


class ListingViewSet(viewsets.ModelViewSet):
    """Provides CRUD operations for Listings"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """Provides CRUD operations for Bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
