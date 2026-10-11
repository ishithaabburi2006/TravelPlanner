# Travel Planner

Travel Planner is a React/Vite web client and Spring Boot REST API backed by MySQL. It supports public destination and attraction discovery, JWT-based accounts, personal itineraries, locally recorded booking details, and an admin dashboard.

## Requirements

- Java 21
- Maven 3.9+
- Node.js 20.19+ or 22.12+
- MySQL 8+

## Local setup

1. Create a MySQL database and least-privilege application account. For a new database, select it and apply `database/schema.sql`; for an existing database, back it up and follow the one-time migration instructions in [database setup](docs/DEPLOYMENT_GUIDE.md).
2. Copy `backend/.env.example` to `backend/.env`; set a local database password, a strong Base64 JWT key, and optional first-admin credentials. Copy `frontend/.env.example` to `frontend/.env` if the API is not at its default URL.
3. Start the backend with `./start-backend.sh` from the repository root. The backend validates the schema and will not silently modify database structure.
4. In another terminal, run `./start-frontend.sh` and open `http://localhost:5173`.

To generate a JWT key, run `openssl rand -base64 32`. Never rename the template into the source of record: copy `backend/.env.example` to `backend/.env`, fill in local values, and keep `.env` private. Both local and production startup use `ddl-auto=validate`; apply the appropriate SQL before starting the application.

## Build and tests

```sh
cd backend && mvn clean test && mvn clean package
cd ../frontend && npm ci && npm run build
```

See [test report](docs/TEST_REPORT.md) for what is and is not covered. The project has no end-to-end suite yet.

## Deployment

Dockerfiles are included for the backend and frontend. [Railway deployment instructions](docs/DEPLOYMENT_GUIDE.md#deploy-to-railway) cover the MySQL service, service variables, domains, CORS, and database initialization. Configure secret values directly in Railway; do not upload local `.env` files.

## Implemented behavior and limits

- Password hashing uses BCrypt; API auth uses signed, expiring JWTs with an issuer and USER/ADMIN role validation.
- Users can create, update, delete, and list their own itinerary records. A budget below the matching destination's configured average becomes a PENDING admin request.
- Users can edit a saved trip from the dashboard, including its budget, dates, travellers, and planning notes.
- Booking entries are personal records only. There is no provider, ticketing, or payment integration; a locally saved record is not a reservation confirmation.
- Admin APIs are role-protected and support destination CRUD, booking status updates, pending itinerary review, and guarded user account CRUD.
- Destination/attraction seed content includes estimated distances and travel times. It has not been independently verified as a commercial travel data source; images are remote Unsplash URLs and require source/license review before commercial distribution.
- Admin attraction CRUD, booking editing and travel-date separation, pagination, automatic database migration execution, rate limiting, and end-to-end tests are not implemented.

## Documentation

- [Technical audit](docs/TECHNICAL_AUDIT.md)
- [Security review](docs/SECURITY_REVIEW.md)
- [Test report](docs/TEST_REPORT.md)
- [API reference](docs/API_DOCUMENTATION.md)
- [Deployment guide](docs/DEPLOYMENT_GUIDE.md)
- [Database schema notes](docs/DATABASE_SCHEMA.md)

Do not use the local development profile or demo seed credentials as a production deployment configuration.

## Release packaging

Run `python3 package_release.py` to create `TravelPlanner-release-clean.zip`. The script excludes local `.env` files, dependency folders, build output, IDE files, and existing ZIP archives. Inspect the release contents before sharing it, and rotate any credential that has previously been included in an archive.
