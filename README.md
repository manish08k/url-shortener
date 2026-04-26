 URL Shortener

A simple URL shortener built with FastAPI. Runs locally or on Google Cloud Run.

---

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload

# Open in browser
open http://localhost:8000
```

The `BASE_URL` defaults to `http://localhost:8000`. The frontend is served at `/`.

---

## Deploy to Google Cloud Run

### Prerequisites
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
- A GCP project with Cloud Run and Artifact Registry enabled

### 1. Set your project

```bash
export PROJECT_ID=your-gcp-project-id
export REGION=us-central1
export SERVICE_NAME=url-shortener
```

### 2. Build & push the container

```bash
# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Build and push
gcloud builds submit \
  --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE_NAME}
```

### 3. Deploy to Cloud Run

```bash
gcloud run deploy ${SERVICE_NAME} \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars BASE_URL=https://YOUR-SERVICE-URL.run.app
```

> Replace `https://YOUR-SERVICE-URL.run.app` with the URL shown after the first deploy (you can redeploy once you have it).

### One-step deploy (Cloud Run source deploy)

If you don't want to manage Artifact Registry yourself:

```bash
gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars BASE_URL=https://YOUR-SERVICE-URL.run.app
```

---

## Project Structure

```
url-shortener/
├── main.py          # FastAPI app + routes
├── database.py      # In-memory store
├── utils.py         # Base62 encode/decode
├── templates/
│   └── index.html   # Frontend UI
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Notes

- **Storage is in-memory** — URLs are lost on server restart. For production, swap `database.py` with a Redis or PostgreSQL backend.
- The `BASE_URL` env var controls the domain used in generated short links.
- `BASE62` alphabet is `0-9a-zA-Z` (62 chars), so short codes stay compact.
