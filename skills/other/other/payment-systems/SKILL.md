---
name: payment-systems
description: "Implement payment processing with Stripe, PayPal, and automated billing. Use when integrating payments, building subscription systems, handling webhooks, or managing billing automation."
---

# Payment Systems

## Common Payment Patterns

### Webhook Processing (All Providers)

```python
def handle_webhook_idempotently(event_id, handler):
    """Ensure webhook is processed exactly once."""
    if is_event_processed(event_id):
        return
    try:
        handler()
        mark_event_processed(event_id)
    except Exception as e:
        log_error(e)
        raise  # Provider will retry
```

### Error Handling Wrapper

```python
def payment_api_call(api_function, retries=3):
    """Retry with exponential backoff."""
    for attempt in range(retries):
        try:
            return api_function()
        except (ConnectionError, TimeoutError) as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Key Rules
- **Always verify webhook signatures** before processing
- **Idempotency**: Check event/transaction ID before processing
- **Never handle raw card data** on your server (use tokenization)
- **Amounts in smallest unit** (cents for USD)
- **Metadata**: Link provider objects to your DB records

---

## Stripe Implementation

### Checkout Session (Hosted)

```python
import stripe
stripe.api_key = os.environ['STRIPE_SECRET_KEY']

session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': 'Premium Plan'},
            'unit_amount': 2000,  # $20.00
            'recurring': {'interval': 'month'},
        },
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://app.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://app.com/cancel',
    metadata={'user_id': 'user_456'}
)
```

### Payment Intent (Custom UI)

```python
def create_payment_intent(amount, currency='usd', customer_id=None):
    intent = stripe.PaymentIntent.create(
        amount=amount, currency=currency, customer=customer_id,
        automatic_payment_methods={'enabled': True}
    )
    return intent.client_secret  # Send to frontend
```

Frontend confirmation:
```javascript
const {error, paymentIntent} = await stripe.confirmCardPayment(clientSecret, {
    payment_method: { card: cardElement, billing_details: { name: 'Customer' } }
});
```

### Subscription Creation

```python
def create_subscription(customer_id, price_id):
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{'price': price_id}],
        payment_behavior='default_incomplete',
        payment_settings={'save_default_payment_method': 'on_subscription'},
        expand=['latest_invoice.payment_intent'],
    )
    return {
        'subscription_id': subscription.id,
        'client_secret': subscription.latest_invoice.payment_intent.client_secret
    }
```

### Webhook Handler

```python
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    event = stripe.Webhook.construct_event(
        request.data, request.headers.get('Stripe-Signature'), endpoint_secret
    )

    handlers = {
        'payment_intent.succeeded': handle_successful_payment,
        'payment_intent.payment_failed': handle_failed_payment,
        'customer.subscription.deleted': handle_subscription_canceled,
        'invoice.payment_succeeded': handle_invoice_paid,
        'charge.refunded': handle_refund,
    }

    handler = handlers.get(event['type'])
    if handler:
        handler(event['data']['object'])
    return 'OK', 200
```

### Refunds

```python
stripe.Refund.create(
    payment_intent='pi_xxx',
    amount=500,  # Partial refund in cents; omit for full
    reason='requested_by_customer'  # or 'duplicate', 'fraudulent'
)
```

### Test Cards

| Scenario | Card Number |
|----------|-------------|
| Success | `4242424242424242` |
| Declined | `4000000000000002` |
| 3D Secure | `4000002500003155` |
| Insufficient funds | `4000000000009995` |

### Customer Portal

```python
session = stripe.billing_portal.Session.create(
    customer=customer_id,
    return_url='https://app.com/account',
)
# Redirect to session.url
```

---

## PayPal Implementation

### Smart Buttons (Frontend)

```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<script>
paypal.Buttons({
    createOrder: (data, actions) => actions.order.create({
        purchase_units: [{ amount: { value: '25.00' } }]
    }),
    onApprove: (data, actions) => actions.order.capture().then(details => {
        fetch('/api/paypal/capture', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({orderID: data.orderID})
        });
    })
}).render('#paypal-button-container');
</script>
```

### Server-Side Client

```python
class PayPalClient:
    def __init__(self, client_id, client_secret, mode='sandbox'):
        self.base_url = 'https://api-m.sandbox.paypal.com' if mode == 'sandbox' else 'https://api-m.paypal.com'
        self.access_token = self._get_token(client_id, client_secret)

    def _get_token(self, client_id, client_secret):
        r = requests.post(f"{self.base_url}/v1/oauth2/token",
            headers={"Accept": "application/json"},
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret))
        return r.json()['access_token']

    def _headers(self):
        return {"Content-Type": "application/json", "Authorization": f"Bearer {self.access_token}"}

    def create_order(self, amount, currency='USD'):
        return requests.post(f"{self.base_url}/v2/checkout/orders",
            headers=self._headers(),
            json={"intent": "CAPTURE", "purchase_units": [{"amount": {"currency_code": currency, "value": str(amount)}}]}
        ).json()

    def capture_order(self, order_id):
        return requests.post(f"{self.base_url}/v2/checkout/orders/{order_id}/capture",
            headers=self._headers()).json()

    def refund(self, capture_id, amount=None, note=None):
        payload = {}
        if amount: payload["amount"] = {"value": str(amount), "currency_code": "USD"}
        if note: payload["note_to_payer"] = note
        return requests.post(f"{self.base_url}/v2/payments/captures/{capture_id}/refund",
            headers=self._headers(), json=payload).json()
```

### IPN Verification

```python
@app.route('/ipn', methods=['POST'])
def handle_ipn():
    ipn_data = request.form.to_dict()

    # Verify with PayPal
    verify_data = {**ipn_data, 'cmd': '_notify-validate'}
    response = requests.post('https://ipnpb.paypal.com/cgi-bin/webscr', data=verify_data)
    if response.text != 'VERIFIED':
        return 'Verification failed', 400

    # Idempotency check
    if is_transaction_processed(ipn_data.get('txn_id')):
        return 'Already processed', 200

    handlers = {
        'Completed': handle_payment_completed,
        'Refunded': handle_refund,
        'Reversed': handle_chargeback,
    }
    handler = handlers.get(ipn_data.get('payment_status'))
    if handler:
        handler(ipn_data)
    return 'OK', 200
```

### Subscription Plans

```python
def create_subscription_plan(client, name, amount, interval='MONTH'):
    return requests.post(f"{client.base_url}/v1/billing/plans",
        headers=client._headers(),
        json={
            "product_id": "PRODUCT_ID",
            "name": name,
            "billing_cycles": [{
                "frequency": {"interval_unit": interval, "interval_count": 1},
                "tenure_type": "REGULAR", "sequence": 1, "total_cycles": 0,
                "pricing_scheme": {"fixed_price": {"value": str(amount), "currency_code": "USD"}}
            }],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "payment_failure_threshold": 3
            }
        }).json()
```

---

## Billing & Subscription Workflows

### Subscription State Machine

```
trial -> active -> past_due -> canceled
                -> paused -> active
```

### Billing Cycle Processing

```python
class BillingEngine:
    def process_billing_cycle(self, subscription):
        if datetime.now() < subscription.current_period_end:
            return

        invoice = self.generate_invoice(subscription)
        result = self.charge_customer(subscription.customer_id, invoice.total)

        if result.success:
            invoice.mark_paid()
            subscription.advance_billing_period()
        else:
            subscription.mark_past_due()
            self.start_dunning(subscription, invoice)
```

### Dunning (Failed Payment Recovery)

```python
class DunningManager:
    retry_schedule = [
        {'days': 3, 'template': 'payment_failed_first'},
        {'days': 7, 'template': 'payment_failed_reminder'},
        {'days': 14, 'template': 'payment_failed_final'},
    ]

    def retry_payment(self, attempt):
        result = self.charge_customer(attempt.customer_id, attempt.amount)
        if result.success:
            attempt.invoice.mark_paid()
            attempt.subscription.status = 'active'
        elif attempt.number >= len(self.retry_schedule):
            attempt.subscription.cancel(at_period_end=False)
        else:
            next_config = self.retry_schedule[attempt.number]
            attempt.next_retry = datetime.now() + timedelta(days=next_config['days'])
            self.send_email(attempt.customer, next_config['template'])
```

### Proration Calculator

```python
def calculate_proration(old_plan, new_plan, period_start, period_end, change_date):
    total_days = (period_end - period_start).days
    days_remaining = (period_end - change_date).days
    unused = (old_plan.amount / total_days) * days_remaining
    new_charge = (new_plan.amount / total_days) * days_remaining
    return {'credit': -unused, 'charge': new_charge, 'net': new_charge - unused}

def calculate_seat_proration(current, new, price_per_seat, period_start, period_end, change_date):
    total_days = (period_end - period_start).days
    days_remaining = (period_end - change_date).days
    additional = new - current
    return max(0, (additional * price_per_seat / total_days) * days_remaining)
```

### Usage-Based Billing

```python
def calculate_tiered_pricing(total_usage, tiers):
    """Tiers: [{'up_to': 100, 'from': 0, 'unit_price': 0.10}, ...]"""
    charge, remaining = 0, total_usage
    for tier in sorted(tiers, key=lambda x: x['up_to']):
        tier_usage = min(remaining, tier['up_to'] - tier['from'])
        charge += tier_usage * tier['unit_price']
        remaining -= tier_usage
        if remaining <= 0:
            break
    return charge
```

### Tax Calculation

```python
TAX_RATES = {
    'US_CA': (0.0725, 'Sales Tax'), 'US_NY': (0.04, 'Sales Tax'),
    'GB': (0.20, 'VAT'), 'DE': (0.19, 'VAT'), 'FR': (0.20, 'VAT'),
    'AU': (0.10, 'GST'),
}

def calculate_tax(amount, customer):
    jurisdiction = f"US_{customer.state}" if customer.country == 'US' else customer.country
    rate, tax_type = TAX_RATES.get(jurisdiction, (0, 'Tax'))
    return {'amount': amount * rate, 'rate': rate, 'type': tax_type}
```
