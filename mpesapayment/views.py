from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from store.models import Order
from .models import MpesaPayment
from .utilis import get_mpesa_token, generate_password, get_timestamp
import requests
import json


# ----------------------------
# Initiate STK Push Payment
# ----------------------------
@login_required
def initiate_payment(request, order_id):
    """
    Initiates an M-Pesa STK Push for a specific order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = max(order.total_amount, 10)  # Sandbox minimum is 10 KES

        # Normalize phone number to 2547XXXXXXXX
        phone_number = phone_number.strip()
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('7'):
            phone_number = '254' + phone_number
        elif not phone_number.startswith('254'):
            messages.error(request, 'Invalid phone number format.')
            return redirect('store:order_detail', order_id=order.id)

        try:
            # Generate access token and STK password
            access_token = get_mpesa_token()
            timestamp = get_timestamp()
            password = generate_password(settings.MPESA_SHORTCODE, settings.MPESA_PASSKEY, timestamp)

            stk_url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
            payload = {
                "BusinessShortCode": settings.MPESA_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": int(phone_number),
                "PartyB": int(settings.MPESA_SHORTCODE),
                "PhoneNumber": int(phone_number),
                "CallBackURL": settings.MPESA_CALLBACK_URL,
                "AccountReference": str(order.id),
                "TransactionDesc": f"Payment for Order #{order.id}"
            }
            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

            # Send STK Push request
            result = requests.post(stk_url, json=payload, headers=headers).json()
            print("STK Push Response:", json.dumps(result, indent=4))

            # Save the payment attempt as pending
            status = 'pending'
            if result.get('ResponseCode') != '0':
                status = 'failed'
                messages.error(request, f"Failed to initiate M-Pesa payment: {result.get('errorMessage') or result.get('ResponseDescription', 'Unknown error')}")
            else:
                messages.success(request, "STK Push sent. Complete payment on your phone.")

            MpesaPayment.objects.create(
                order=order,
                amount=amount,
                phone_number=phone_number,
                response=result,
                status=status
            )

        except Exception as e:
            messages.error(request, f'Error connecting to M-Pesa: {str(e)}')

        return redirect('store:order_detail', order_id=order.id)

    return render(request, 'mpesapayment/mpesa_payment.html', {'order': order})


# ----------------------------
# M-Pesa Payment Callback
# ----------------------------
@csrf_exempt
def payment_callback(request):
    """
    Receives M-Pesa payment callback and updates order/payment records.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        print("M-Pesa Callback Received:", json.dumps(data, indent=4))

        callback = data.get('Body', {}).get('stkCallback', {})
        result_code = callback.get('ResultCode')
        callback_items = callback.get('CallbackMetadata', {}).get('Item', [])

        # Default values
        order = None
        amount = 0
        receipt = ''
        phone = ''
        status = 'failed'

        if result_code == 0:
            # Successful payment
            amount = next((item['Value'] for item in callback_items if item['Name'] == 'Amount'), 0)
            receipt = next((item['Value'] for item in callback_items if item['Name'] == 'MpesaReceiptNumber'), '')
            phone = next((item['Value'] for item in callback_items if item['Name'] == 'PhoneNumber'), '')
            order_id = next((item['Value'] for item in callback_items if item['Name'] == 'BillRefNumber'), None)

            if order_id:
                order = Order.objects.filter(id=order_id).first()
                if order:
                    order.status = 'paid'
                    order.save()
                    status = 'completed'

        else:
            # Failed or cancelled payment
            phone = callback_items[0]['Value'] if callback_items else ''
            result_desc = callback.get('ResultDesc', 'Failed transaction')
            print(f"Payment failed: ResultCode={result_code}, Description={result_desc}, Phone={phone}")

        # Save MpesaPayment record
        MpesaPayment.objects.create(
            order=order,
            amount=amount,
            phone_number=phone,
            mpesa_receipt=receipt,
            response=data,
            status=status
        )

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

    except json.JSONDecodeError:
        print("Invalid JSON received in callback")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)


# ----------------------------
# Optional: Test/Standalone STK Push
# ----------------------------
@login_required
def initiate_stk_push(request):
    """
    Standalone STK Push test (replace phone_number and amount for testing).
    """
    phone_number = "2547XXXXXXXX"  # Replace with actual number
    amount = 1  # Replace with amount to charge

    try:
        token = get_mpesa_token()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    timestamp = get_timestamp()
    password = generate_password(settings.MPESA_SHORTCODE, settings.MPESA_PASSKEY, timestamp)

    stk_push_url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": int(phone_number),
        "PartyB": int(settings.MPESA_SHORTCODE),
        "PhoneNumber": int(phone_number),
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "Test123",
        "TransactionDesc": "Payment Test"
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.post(stk_push_url, json=payload, headers=headers)
    return JsonResponse(response.json())
