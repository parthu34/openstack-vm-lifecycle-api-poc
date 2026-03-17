# Roadmap and Backlog

This document describes the next logical steps beyond the assessment time box.

## 1. Short-Term Improvements

### Authentication and authorization
Add API authentication and role-based access control so lifecycle operations are protected.

### Persistent storage
Store VM operation history and request audit data in a database such as PostgreSQL.

### Better OpenStack integration validation
Add integration tests against a real dev or staging OpenStack environment.

### Improved response models
Include richer infrastructure details such as addresses, availability zone, project ID, and timestamps.

## 2. Medium-Term Enhancements

### Async job execution
Move long-running cloud operations into background workers or a task queue.

### Retry and resilience patterns
Add retry policies, timeout handling, and better cloud error categorization.

### Metrics and monitoring
Expose Prometheus metrics and add dashboards/alerts for request latency, failures, and operation counts.

### Idempotency support
Protect state-changing endpoints from duplicate client retries.

### Request and audit persistence
Store request IDs, operation results, and failure details for operational auditing.

## 3. Platform/Infrastructure Improvements

### Container deployment manifests
Add Kubernetes manifests or Helm charts for deployment.

### Infrastructure as Code
Add Terraform or similar automation for deployment environments.

### Secret management
Move sensitive cloud configuration to a secure secret store.

### Environment-specific configuration
Separate local, dev, staging, and production settings more clearly.

## 4. API Improvements

### Volume management endpoints
Add:
- attach volume
- detach volume
- create snapshot
- restore snapshot

### Network operations
Add network interface attach/detach workflows.

### Pagination and filtering
Support filters for VM status, project, name, and creation date.

### OpenAPI enrichment
Add richer examples, tags, and endpoint descriptions.

## 5. Reliability and Testing Backlog

### More unit tests
Expand test coverage around provider edge cases and cloud failures.

### Contract tests
Validate API response consistency more formally.

### Integration tests
Run selected tests against a disposable or sandbox OpenStack environment.

### Load and performance testing
Measure how the service behaves under concurrent lifecycle requests.

## 6. Production Readiness Backlog

### Health/readiness split
Separate liveness and readiness checks.

### Centralized logging pipeline
Ship logs to a log platform such as ELK or Loki.

### Alerting
Add alerts for high failure rates or cloud operation latency spikes.

### Operational runbooks
Document failure scenarios and common remediation steps.
