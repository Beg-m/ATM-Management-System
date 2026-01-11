# ATM Management System - Mobile Application

Mobile ATM application developed for Python Programming final project.

## Features

- Modern GUI application developed with Kivy framework
- Touch-friendly interface suitable for mobile devices
- Full-featured ATM operations (view balance, deposit, withdraw)

## Installation

### Requirements
- Python 3.7 or higher

### Installation Steps
1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Kivy:
```bash
pip install -r requirements.txt
```

or

```bash
pip install kivy
```

3. Run the application:
```bash
python3 atm_mobile.py
```

**Note:** Make sure to activate the virtual environment before running the application. If you're not using a virtual environment, you may need to use `pip install --user kivy` instead.

## Test User Credentials

| Card Number | Password | Balance |
|-------------|----------|---------|
| 1234567890  | 1234     | $5000   |
| 2345678901  | 2345     | $3500   |
| 3456789012  | 3456     | $8200   |
| 4567890123  | 4567     | $1200   |
| 5678901234  | 5678     | $9500   |

## Features

- ✅ Login with card number and password
- ✅ System lock after 3 wrong attempts
- ✅ View balance
- ✅ Deposit money (negative/zero amount validation)
- ✅ Withdraw money (with balance check)
- ✅ All transactions are saved to `transactions.txt` file
- ✅ Error handling and user-friendly messages

## File Structure

- `atm_mobile.py` - Mobile ATM application developed with Kivy
- `requirements.txt` - Python dependencies (Kivy)
- `transactions.txt` - Transaction records (created when the application is run)

## Notes

- The mobile application also runs on desktop computers (400x700 pixel window)
- To install on real mobile devices, Buildozer or KivyMD can be used
- All transactions are saved to `transactions.txt` with date-time, card number, transaction type, amount, and current balance information
