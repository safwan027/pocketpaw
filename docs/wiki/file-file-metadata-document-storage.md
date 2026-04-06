# file — File metadata document storage

> Defines the FileObj document model for storing file metadata in MongoDB via Beanie ODM. Actual file bytes are stored in cloud object storage (S3/GCS/local), while this model maintains references, ownership, and access control metadata. Serves as the database schema for file tracking in the pocketPaw cloud system.

**Categories:** data models, cloud storage, document persistence, file management  
**Concepts:** FileObj, Document, Indexed field, Beanie ODM, file metadata, cloud storage decoupling, owner-based access control, provider pattern, MongoDB collection, pydantic validation  
**Words:** 213 | **Version:** 1

---

## Purpose
Provides a Beanie Document class to persist file metadata without storing actual file contents in the database. Enables efficient file management by decoupling metadata (stored in MongoDB) from binary data (stored in S3/GCS).

## Key Classes

### FileObj(Document)
MongoDB document model for file metadata.

**Fields:**
- `owner` (Indexed[str]): File owner identifier, indexed for fast lookup
- `file_name` (str): Human-readable filename
- `bucket` (str): Cloud storage bucket name
- `provider` (str): Storage provider, constrained to 'gcs', 's3', or 'local'
- `path_in_bucket` (str): Full path within the bucket
- `mime_type` (str): MIME type, defaults to empty string
- `size` (int): File size in bytes, defaults to 0
- `public` (bool): Access control flag, defaults to False

**Settings:**
- MongoDB collection name: 'files'

## Dependencies
- `beanie`: Document ODM and Indexed field type
- `pydantic`: Field validation with regex pattern support

## Usage Examples
```python
# Create file metadata document
file_doc = FileObj(
    owner='user_123',
    file_name='report.pdf',
    bucket='pocketpaw-files',
    provider='s3',
    path_in_bucket='uploads/2024/report.pdf',
    mime_type='application/pdf',
    size=2048576,
    public=False
)
await file_doc.insert()

# Query by owner (indexed)
user_files = await FileObj.find(FileObj.owner == 'user_123').to_list()
```

## Architecture Notes
- Follows separation of concerns: metadata in MongoDB, binary in cloud storage
- Indexed owner field optimizes user-centric file queries
- Provider pattern allows multi-cloud support
- Pre-signed URLs can be generated from path_in_bucket on-demand

---

## Related

- [eecloudworkspace-workspace-module-initialization](eecloudworkspace-workspace-module-initialization.md)
