# db — MongoDB Connection and Beanie ODM Initialization

> This module manages MongoDB connectivity and Beanie ODM initialization for the pocketPaw cloud backend. It provides a global async MongoDB client and initialization utilities for document model registration, ensuring consistent database access across the application.

**Categories:** database, infrastructure, cloud backend  
**Concepts:** async MongoDB client, Beanie ODM initialization, global state management, URI parsing, lifecycle management, document model registration, Beanie ODM  
**Words:** 220 | **Version:** 2

---

## Purpose
Provides centralized MongoDB connection management using PyMongo's AsyncMongoClient and Beanie ODM framework. Handles initialization of all document models and lifecycle management of the database connection.

## Key Functions

### `async init_cloud_db(mongo_uri: str)`
Initializes the Beanie ODM with all document models from `ee.cloud.models.ALL_DOCUMENTS`. Extracts the database name from the MongoDB URI and establishes the async client connection. Logs initialization details including model count.

**Parameters:**
- `mongo_uri` (str): MongoDB connection string, defaults to `"mongodb://localhost:27017/paw-cloud"`

### `async close_cloud_db()`
Closes the global MongoDB client and resets it to None. Should be called during application shutdown.

### `get_client() -> AsyncMongoClient | None`
Returns the current MongoDB client instance, or None if not initialized. Provides read-only access to the global client for other modules.

## Dependencies
- **beanie**: ODM framework for async MongoDB operations
- **pymongo**: Async MongoDB driver
- **logging**: Standard library for logging initialization events

## Global State
- `_client`: Module-level AsyncMongoClient instance (None until initialized)

## Usage Pattern
```python
# Initialization at application startup
await init_cloud_db()

# Later usage in other modules
client = get_client()

# Cleanup at shutdown
await close_cloud_db()
```

## Design Notes
- Uses async/await for non-blocking database operations
- Global client pattern allows stateless access from any module
- URI parsing handles optional database names and query parameters
- Type hints support Python 3.10+ union syntax (|)