import hashlib
import requests
import stripe

class PaymentGatewayHub:
    def __init__(self):
        stripe.api_key = "sk_test_mock_stripe"
        self.payfast_merchant_id = "10000100"
        self.payfast_merchant_key = "46f0cd6945b6a"
        self.ozow_site_code = "CAR-NEX-001"
        self.ozow_private_key = "9a73e13d98b"

    def initiate_stripe_checkout(self, amount_usd: float, success_url: str, cancel_url: str):
        """Processes global cards via Stripe Checkout."""
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'CareerNexus Pro Package Suite'},
                    'unit_amount': int(amount_usd * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return {"gateway": "Stripe", "checkout_url": session.url}

    def generate_payfast_form_payload(self, amount_zar: float, item_name: str, return_url: str):
        """Generates verified payloads and MD5 signature generation strings for PayFast integration."""
        payload = {
            "merchant_id": self.payfast_merchant_id,
            "merchant_key": self.payfast_merchant_key,
            "return_url": return_url,
            "amount": f"{amount_zar:.2f}",
            "item_name": item_name
        }
        # Construct MD5 generation signature
        param_str = f"merchant_id={payload['merchant_id']}&merchant_key={payload['merchant_key']}&return_url={payload['return_url']}&amount={payload['amount']}&item_name={payload['item_name']}"
        payload["signature"] = hashlib.md5(param_str.encode('utf-8')).hexdigest()
        return {"gateway": "PayFast", "post_url": "https://sandbox.payfast.co.za/eng/process", "payload": payload}

    def initiate_ozow_instant_eft(self, amount_zar: float, bank_reference: str, cancel_url: str, success_url: str):
        """Calculates SHA-512 checks across sequential parameters for Ozow Instant EFT integration."""
        site_code = self.ozow_site_code
        country_code = "ZA"
        currency_code = "ZAR"
        amount = f"{amount_zar:.2f}"
        
        # Explicit sequential concatenation rules for Ozow hashing
        raw_string = f"{site_code}{bank_reference}{amount}{currency_code}{country_code}{self.ozow_private_key}".lower()
        hash_check = hashlib.sha512(raw_string.encode('utf-8')).hexdigest()
        
        return {
            "gateway": "Ozow",
            "endpoint": "https://pay.ozow.com/",
            "payload": {
                "SiteCode": site_code,
                "CountryCode": country_code,
                "CurrencyCode": currency_code,
                "Amount": amount,
                "TransactionReference": bank_reference,
                "HashCheck": hash_check
            }
        }
