import time
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer

CHAPA_API_URL = 'https://api.chapa.co/v1/transaction/initialize'
CHAPA_VERIFY_URL = 'https://api.chapa.co/v1/transaction/verify'

@api_view(['POST'])
def initiate_payment(request):
    amount = request.data.get('amount')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not amount or not email or not first_name or not last_name:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    tx_ref = 'txn_' + str(int(time.time()))  # Generate unique transaction reference
    data = {
        'amount': amount,
        'currency': 'ETB',
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'tx_ref': tx_ref,
        'callback_url': request.build_absolute_uri('/payments/callback/'),
    }
    headers = {
        'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'
    }
    response = requests.post(CHAPA_API_URL, json=data, headers=headers)
    response_data = response.json()

    if response_data['status'] == 'success':
        # payment = Payment.objects.create(
        #     amount=amount,
        #     transaction_id=response_data['data']['tx_ref'],
        #     status='initiated'
        # )
        return Response(response_data['data'], status=status.HTTP_201_CREATED)
    else:
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def payment_callback(request):
    tx_ref = request.query_params.get('tx_ref')
    if not tx_ref:
        return Response({'error': 'Transaction reference is required'}, status=status.HTTP_400_BAD_REQUEST)

    headers = {
        'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'
    }
    response = requests.get(f'{CHAPA_VERIFY_URL}/{tx_ref}', headers=headers)
    response_data = response.json()

    if response.status_code != 200 or response_data['status'] != 'success':
        return Response({'status': 'Payment verification failed', 'details': response_data}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
        if response_data['data']['status'] == 'success':
            payment.status = 'completed'
        else:
            payment.status = 'failed'
        payment.save()
        return Response({'status': f'Payment {payment.status}'}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)