## Seed the Database

To populate the database with sample listings:

```bash
python manage.py seed

# alx_travel_app_0x02

## Payment Integration with Chapa API

- Users can make payments for bookings via Chapa.
- Payment statuses are stored in the `Payment` model.
- Workflow:
  1. Initiate Payment (`/listings/initiate-payment/`)
  2. Redirect user to Chapa checkout URL.
  3. Verify Payment (`/listings/verify-payment/`)
- Tested using Chapa Sandbox API...

