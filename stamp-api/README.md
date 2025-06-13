# Stamp App Backend

This is the backend for the Stamp App, a FastAPI-based service that allows users to upload, extract, and stamp images onto PDF files. It supports user authentication, Stripe-based subscriptions, and secure file handling.

## Features

- **User Registration & Login** (JWT authentication)
- **PDF Stamping**: Upload a PDF and a stamp image, and apply the stamp to the PDF
- **Stamp Extraction**: Extract stamp images from uploaded files
- **Stripe Subscription Integration**: Manage user subscriptions and payments
- **MongoDB Storage**: User and subscription data stored with MongoEngine
- **Secure File Handling**: Temporary files are cleaned up after processing
- **CORS Support**: For frontend integration

## Tech Stack

- **Python 3.12+**
- **FastAPI**
- **MongoEngine** (MongoDB)
- **Stripe**
- **bcrypt** (password hashing)
- **Uvicorn** (ASGI server)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/stamp-app.git
cd stamp-app/stamp-backend
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the `app/` directory with the following:

```
SECRET_KEY=your_secret_key
MONGODB_URI=mongodb://localhost:27017/stampapp
STRIPE_API_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Auth

- `POST /auth/register` — Register a new user
- `POST /auth/login` — Login and receive a JWT token

### Stamps

- `POST /stamps/extract_stamp/` — Extract a stamp image from an uploaded file (auth required)
- `POST /stamps/stamp-pdf/` — Stamp a PDF with an uploaded image (auth required)

### Subscription

- `POST /subscription/create` — Create a Stripe subscription (auth required)
- `POST /webhook/stripe` — Stripe webhook endpoint

## Usage

- Use the JWT token from `/auth/login` in the `Authorization: Bearer <token>` header for protected endpoints.
- Integrate with Stripe for subscription management.

## Folder Structure

```
stamp-backend/
├── app/
│   ├── api/
│   ├── helpers/
│   ├── models/
│   ├── services/
│   ├── main.py
│   └── ...
├── requirements.txt
└── README.md
```

## License

MIT

---

**Note:**  
This backend is designed to work with a separate frontend (e.g., React).  
Make sure MongoDB and Stripe credentials are set up correctly before running the app.