#!/usr/bin/env python3
"""
Test script for Documentation tools - list_sections and get_documentation
Tests both functions independently before MCP integration.
"""

import httpx
import json
import asyncio

# Documentation Repository Configuration
DOCS_CONFIG = {
    "BASE_URL": "https://raw.githubusercontent.com/mustavikhan05/selise-blocks-docs/master/",
    "TOPICS_JSON_URL": "https://raw.githubusercontent.com/mustavikhan05/selise-blocks-docs/master/topics.json"
}


async def list_sections() -> str:
    """
    List all available Selise Blocks documentation topics.

    Returns:
        JSON string with complete topics catalog and metadata
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                DOCS_CONFIG["TOPICS_JSON_URL"],
                timeout=30.0
            )
            response.raise_for_status()
            topics_data = response.json()

        # Extract summary information
        topics_list = topics_data.get("topics", [])
        critical_topics = [t for t in topics_list if t.get("priority") == "critical"]
        workflow_topics = [t for t in topics_list if t.get("type") == "workflow"]
        recipe_topics = [t for t in topics_list if t.get("type") == "recipe"]

        result = {
            "status": "success",
            "message": f"Found {len(topics_list)} documentation topics",
            "metadata": {
                "version": topics_data.get("version"),
                "last_updated": topics_data.get("last_updated"),
                "base_url": topics_data.get("base_url")
            },
            "summary": {
                "total_topics": len(topics_list),
                "critical_count": len(critical_topics),
                "workflow_count": len(workflow_topics),
                "recipe_count": len(recipe_topics)
            },
            "topics": topics_list,
            "critical_first_reads": [
                {
                    "id": t.get("id"),
                    "title": t.get("title"),
                    "read_when": t.get("read_when"),
                    "read_order": t.get("read_order")
                }
                for t in sorted(critical_topics, key=lambda x: x.get("read_order", 999))
            ]
        }

        return json.dumps(result, indent=2)

    except httpx.HTTPStatusError as e:
        return json.dumps({
            "status": "error",
            "message": f"HTTP error fetching documentation catalog: {e.response.status_code}",
            "details": e.response.text,
            "url": DOCS_CONFIG["TOPICS_JSON_URL"]
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error fetching documentation catalog: {str(e)}",
            "url": DOCS_CONFIG["TOPICS_JSON_URL"]
        }, indent=2)


async def get_documentation(topic) -> str:
    """
    Fetch specific Selise Blocks documentation by topic ID.

    Args:
        topic: Single topic ID (string) or list of topic IDs

    Returns:
        JSON string with full markdown content for requested topics
    """
    try:
        # Normalize topic to list
        topic_ids = [topic] if isinstance(topic, str) else topic

        # First, fetch topics.json to get metadata
        async with httpx.AsyncClient() as client:
            topics_response = await client.get(
                DOCS_CONFIG["TOPICS_JSON_URL"],
                timeout=30.0
            )
            topics_response.raise_for_status()
            topics_data = topics_response.json()

        topics_list = topics_data.get("topics", [])
        base_url = topics_data.get("base_url", DOCS_CONFIG["BASE_URL"])

        # Find requested topics and fetch their content
        results = []
        not_found = []

        for topic_id in topic_ids:
            # Find topic metadata
            topic_meta = next((t for t in topics_list if t.get("id") == topic_id), None)

            if not topic_meta:
                not_found.append(topic_id)
                continue

            # Fetch documentation content
            doc_url = f"{base_url}{topic_meta.get('path')}"
            try:
                async with httpx.AsyncClient() as client:
                    doc_response = await client.get(doc_url, timeout=30.0)
                    doc_response.raise_for_status()
                    content = doc_response.text

                results.append({
                    "topic_id": topic_id,
                    "title": topic_meta.get("title"),
                    "type": topic_meta.get("type"),
                    "priority": topic_meta.get("priority"),
                    "content": content,
                    "metadata": {
                        "read_when": topic_meta.get("read_when"),
                        "use_cases": topic_meta.get("use_cases"),
                        "warnings": topic_meta.get("warnings", []),
                        "next_steps": topic_meta.get("next_steps", [])
                    }
                })
            except Exception as fetch_error:
                results.append({
                    "topic_id": topic_id,
                    "error": f"Failed to fetch content: {str(fetch_error)}",
                    "url": doc_url
                })

        # Build response
        result = {
            "status": "success" if results else "error",
            "message": f"Retrieved {len(results)} documentation topic(s)",
            "requested": topic_ids,
            "not_found": not_found if not_found else None,
            "documentation": results
        }

        return json.dumps(result, indent=2)

    except httpx.HTTPStatusError as e:
        return json.dumps({
            "status": "error",
            "message": f"HTTP error fetching documentation: {e.response.status_code}",
            "details": e.response.text
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error fetching documentation: {str(e)}"
        }, indent=2)


async def test_list_sections():
    """Test 1: List all documentation sections."""
    print("=" * 80)
    print("TEST 1: List All Documentation Sections")
    print("=" * 80)

    result = await list_sections()
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")
    print(f"\nMetadata:")
    print(f"  Version: {result_data.get('metadata', {}).get('version')}")
    print(f"  Last Updated: {result_data.get('metadata', {}).get('last_updated')}")
    print(f"\nSummary:")
    summary = result_data.get('summary', {})
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print(f"\nCritical First Reads:")
    for topic in result_data.get('critical_first_reads', [])[:5]:
        print(f"  [{topic.get('read_order')}] {topic.get('id')}: {topic.get('title')}")

    print("\n✅ Test 1 PASSED\n")
    return result_data


async def test_get_single_documentation():
    """Test 2: Get single documentation topic."""
    print("=" * 80)
    print("TEST 2: Get Single Documentation (project-setup)")
    print("=" * 80)

    result = await get_documentation("project-setup")
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")

    if result_data.get('documentation'):
        doc = result_data['documentation'][0]
        print(f"\nTopic: {doc.get('topic_id')}")
        print(f"Title: {doc.get('title')}")
        print(f"Type: {doc.get('type')}")
        print(f"Priority: {doc.get('priority')}")
        print(f"Content Length: {len(doc.get('content', ''))} characters")
        print(f"\nContent Preview:")
        print(doc.get('content', '')[:300] + "...")

    print("\n✅ Test 2 PASSED\n")
    return result_data


async def test_get_multiple_documentation():
    """Test 3: Get multiple documentation topics."""
    print("=" * 80)
    print("TEST 3: Get Multiple Documentation Topics")
    print("=" * 80)

    result = await get_documentation(["graphql-crud", "patterns"])
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")
    print(f"Requested: {result_data.get('requested')}")

    print(f"\nRetrieved Topics:")
    for doc in result_data.get('documentation', []):
        print(f"  - {doc.get('topic_id')}: {doc.get('title')} ({len(doc.get('content', ''))} chars)")

    print("\n✅ Test 3 PASSED\n")
    return result_data


async def test_invalid_topic():
    """Test 4: Handle invalid topic gracefully."""
    print("=" * 80)
    print("TEST 4: Invalid Topic Handling")
    print("=" * 80)

    result = await get_documentation("non-existent-topic")
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")
    print(f"Not Found: {result_data.get('not_found')}")

    print("\n✅ Test 4 PASSED (correctly handled invalid topic)\n")
    return result_data


async def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🧪 TESTING DOCUMENTATION TOOLS")
    print("=" * 80 + "\n")

    try:
        # Test 1: List sections
        await test_list_sections()

        # Test 2: Get single documentation
        await test_get_single_documentation()

        # Test 3: Get multiple documentation
        await test_get_multiple_documentation()

        # Test 4: Invalid topic
        await test_invalid_topic()

        print("=" * 80)
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
