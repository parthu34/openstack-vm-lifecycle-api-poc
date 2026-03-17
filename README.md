# OpenStack VM Lifecycle API

A proof-of-concept FastAPI service for managing OpenStack VM lifecycle operations.

This project was built as a time-boxed backend/platform engineering assessment. It demonstrates API design, Python backend development, service layering, provider abstraction, local mock-mode execution, Docker-based packaging, and automated test execution with GitHub Actions.

## Project Goals

The objective of this project is to expose REST API endpoints for common VM lifecycle operations while keeping the implementation easy to run locally and easy to extend toward real OpenStack integration.

The project supports two provider modes:

* `mock` — local in-memory provider for development, demos, and tests
* `openstack` — real provider using `openstacksdk`

## Why This Design

The application uses a provider abstraction so the API and service layers do not depend directly on a live OpenStack environment.

This approach gives three advantages:

1. The prototype runs locally without cloud credentials
2. Tests stay deterministic and fast
3. The same API surface can later be backed by a real OpenStack cloud

## Key Features

* FastAPI REST API for VM lifecycle operations
* Typed request and response models using Pydantic
* Service layer for lifecycle rules and orchestration
* Mock OpenStack provider for local development
* Real OpenStack provider skeleton using `openstacksdk`
* Structured error responses
* Request ID middleware and structured logging
* Dockerfile and Docker Compose support
* Minimal GitHub Actions CI for automated test execution

## API Endpoints

### Health

* `GET /health`

### VM Lifecycle

* `POST /api/v1/vms`
* `GET /api/v1/vms`
* `GET /api/v1/vms/{vm_id}`
* `POST /api/v1/vms/{vm_id}/start`
* `POST /api/v1/vms/{vm_id}/stop`
* `POST /api/v1/vms/{vm_id}/reboot`
* `PATCH /api/v1/vms/{vm_id}/metadata`
* `DELETE /api/v1/vms/{vm_id}`

## Example Request

### Create a VM

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/vms" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "demo-vm",
    "image": "ubuntu-22.04",
    "flavor": "m1.small",
    "network": "private-net",
    "key_name": "demo-key",
    "metadata": {
      "owner": "parth",
      "env": "dev"
    }
  }'
```

## Example Response

```json
{
  "id": "generated-vm-id",
  "name": "demo-vm",
  "status": "ACTIVE",
  "image": "ubuntu-22.04",
  "flavor": "m1.small",
  "network": "private-net",
  "key_name": "demo-key",
  "metadata": {
    "owner": "parth",
    "env": "dev"
  }
}
```

## Project Structure

```text
openstack-vm-lifecycle-api-poc/
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── models/
│   ├── providers/
│   └── services/
├── docs/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Local Development

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 3. Start the application

```bash
uvicorn app.main:app --reload
```

### 4. Open the service

* API: `http://127.0.0.1:8000`
* Swagger UI: `http://127.0.0.1:8000/docs`
* Health check: `http://127.0.0.1:8000/health`

## Running Tests

```bash
pytest
```

## Running with Docker

### Build and run with Compose

```bash
docker compose up --build
```

### Stop

```bash
docker compose down
```

## Provider Modes

### Mock mode (default)

Use this for local development and tests.

```env
PROVIDER_MODE=mock
```

### OpenStack mode

Use this only when valid OpenStack configuration is available.

```env
PROVIDER_MODE=openstack
OPENSTACK_CLOUD=mycloud
OPENSTACK_REGION_NAME=RegionOne
```

The real provider is designed to work with OpenStack SDK connection/config patterns and requires valid cloud credentials or configuration outside this repository.

## Error Response Format

The API returns structured errors in this shape:

```json
{
  "error": {
    "code": "vm_not_found",
    "message": "VM 'missing-vm' was not found",
    "details": {
      "vm_id": "missing-vm"
    }
  }
}
```

## Current Scope and Tradeoffs

This project is intentionally scoped as a proof-of-concept for a 2–4 hour assessment.

### What Is Included

* API design for VM lifecycle operations
* Working local prototype in mock mode
* Real OpenStack integration path
* Tests, Docker support, and CI

### What Is Not Included Yet

* Authentication/authorization
* Persistent database storage
* Background job execution for long-running cloud operations
* Prometheus metrics
* Production deployment manifests

## Design Notes

See the detailed design writeup here:

* Architecture and Design
* Roadmap and Backlog

## How to Review the Project

Recommended review flow:

1. Read this README
2. Run the service locally in mock mode
3. Open `/docs`
4. Create, list, update, and delete a VM through Swagger UI
5. Review `docs/architecture.md`
6. Review the tests and provider abstraction

## Submission Notes

This repository is a proof-of-concept built to demonstrate:

* API design
* Python engineering fundamentals
* Service-oriented structure
* Mock-first development
* OpenStack integration readiness
* Practical DevOps awareness

## License

This project is provided for assessment/demo purposes.
