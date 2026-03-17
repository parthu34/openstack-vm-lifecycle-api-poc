```md
# Architecture and Design

## 1. Overview

This service exposes REST API endpoints for managing VM lifecycle operations in a way that is easy to test locally and easy to evolve toward real OpenStack integration.

The implementation follows a layered design:

- **API layer** — FastAPI route handlers
- **Service layer** — lifecycle rules and orchestration
- **Provider layer** — infrastructure interaction
- **Model layer** — typed request/response contracts
- **Core layer** — configuration, middleware, logging, and exceptions

## 2. High-Level Request Flow

A typical request moves through the system in this order:

1. The HTTP request enters FastAPI
2. Middleware generates or propagates a request ID and measures latency
3. The route handler validates the request using Pydantic models
4. The route handler calls the `VMService`
5. The service applies lifecycle rules and delegates infrastructure work to a provider
6. The provider performs the operation in either mock mode or real OpenStack mode
7. The response is returned as a typed API response model
8. If an error occurs, centralized exception handlers convert it into a structured error response

## 3. Layer Responsibilities

## API Layer

The API layer is intentionally thin.

Its responsibilities:
- receive HTTP requests
- validate input through request models
- call the service layer
- return typed responses

It does **not** contain infrastructure logic or lifecycle rules.

## Service Layer

The `VMService` contains business rules such as:

- do not start an already active VM
- do not stop an already stopped VM
- do not reboot a shutoff VM
- normalize missing-resource behavior into domain exceptions

This makes lifecycle rules easier to test and easier to change without touching the HTTP layer.

## Provider Layer

The provider layer abstracts the infrastructure backend.

### Mock provider
`MockOpenStackProvider` stores VM state in memory and is used for:
- local development
- demos
- automated tests

### Real provider
`RealOpenStackProvider` uses `openstacksdk` and is designed to:
- create SDK connections
- resolve image, flavor, and network resources
- create and wait for servers
- perform lifecycle operations
- update metadata
- delete servers

## 4. Why Provider Abstraction Was Chosen

A direct dependency on live OpenStack infrastructure would make the assessment harder to run, harder to test, and harder to review.

The provider abstraction was chosen so the project could:
- stay runnable without cloud access
- demonstrate realistic API and service design
- keep the OpenStack integration behind a clean interface

This is the main architectural decision in the project.

## 5. Error Handling Design

The service uses domain-specific exceptions such as:
- `VMNotFoundError`
- `InvalidVMStateError`
- `CloudOperationError`
- `CloudResourceLookupError`

A centralized exception handler converts these errors into a uniform JSON response shape.

This improves:
- client experience
- consistency
- troubleshooting
- testability

## 6. Logging and Request Visibility

The service includes:
- request ID correlation
- request timing headers
- structured logs
- service-level operation logs

This was added to show operational awareness and make the service easier to debug.

## 7. Why FastAPI Was Chosen

FastAPI was chosen because it provides:
- clean route definitions
- strong Pydantic integration
- automatic OpenAPI generation
- automatic Swagger UI docs
- simple dependency injection

That made it a strong fit for a time-boxed backend assessment.

## 8. Why Mock-First Development Was Chosen

The project was intentionally built mock-first.

Reasoning:
- the assessment asks for a working prototype
- OpenStack environments are credential- and infrastructure-dependent
- local development should stay fast and deterministic

The mock provider allowed the API contract, service rules, tests, Docker packaging, and CI flow to be completed without depending on a live cloud.

## 9. Main Tradeoffs

Because this is a proof-of-concept, some tradeoffs were made:

### Included
- clear API design
- local working prototype
- provider abstraction
- real provider integration path
- error handling
- logging
- containerization
- CI

### Deferred
- authentication and authorization
- persistent storage
- async job queue
- retries/backoff for cloud failures
- metrics and alerting
- deployment manifests
- live integration testing against a real OpenStack tenant

## 10. SDLC Approach Used

Even within a short assessment window, the implementation followed a lightweight SDLC approach:

1. define project structure
2. define API contracts
3. implement mock working prototype
4. add service layer and exceptions
5. add real provider adapter
6. add logging and middleware
7. containerize the app
8. add CI
9. document architecture and backlog