import pytest

from pocketpaw.vectordb.chroma_adapter import ChromaAdapter

# 1. Add skip if chromadb missing (at the top of the file)
chromadb = pytest.importorskip("chromadb")

@pytest.fixture
def adapter(tmp_path):
    """Fixture to provide a fresh ChromaAdapter for each test."""
    return ChromaAdapter(str(tmp_path / "test_db"))

@pytest.mark.asyncio
async def test_add_and_search(adapter):
    await adapter.add("1", "User likes python")
    results = await adapter.search("python")
    assert "User likes python" in results

# 2. Add more tests as requested by maintainer

@pytest.mark.asyncio
async def test_delete(adapter):
    await adapter.add("2", "To be deleted")
    await adapter.delete("2")
    result = await adapter.get_by_id("2")
    assert result is None

@pytest.mark.asyncio
async def test_get_by_id(adapter):
    await adapter.add("3", "Specific content")
    result = await adapter.get_by_id("3")
    assert result == "Specific content"
    
    # Test getting non-existent ID (Safety check)
    assert await adapter.get_by_id("999") is None

@pytest.mark.asyncio
async def test_search_no_results(adapter):
    # Testing search logic with a query that won't match anything
    results = await adapter.search("nonexistent_keyword_xyz")
    assert results == []

@pytest.mark.asyncio
async def test_duplicate_ids(adapter):
    # This verifies our 'upsert' fix works
    await adapter.add("dup", "First version")
    await adapter.add("dup", "Updated version")
    
    result = await adapter.get_by_id("dup")
    assert result == "Updated version"
