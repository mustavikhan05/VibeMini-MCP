#!/usr/bin/env python3
"""
Test script for Workflow-Specific Documentation Tools
Tests: get_project_setup, get_implementation_checklist, get_dev_workflow,
       get_architecture_patterns, get_common_pitfalls
"""

import httpx
import json
import asyncio

# Documentation Repository Configuration
DOCS_CONFIG = {
    "BASE_URL": "https://raw.githubusercontent.com/mustavikhan05/selise-blocks-docs/master/",
    "TOPICS_JSON_URL": "https://raw.githubusercontent.com/mustavikhan05/selise-blocks-docs/master/topics.json"
}


async def get_documentation(topic):
    """Helper function to fetch documentation (same as in server)."""
    try:
        topic_ids = [topic] if isinstance(topic, str) else topic

        async with httpx.AsyncClient() as client:
            topics_response = await client.get(DOCS_CONFIG["TOPICS_JSON_URL"], timeout=30.0)
            topics_response.raise_for_status()
            topics_data = topics_response.json()

        topics_list = topics_data.get("topics", [])
        base_url = topics_data.get("base_url", DOCS_CONFIG["BASE_URL"])

        results = []
        not_found = []

        for topic_id in topic_ids:
            topic_meta = next((t for t in topics_list if t.get("id") == topic_id), None)

            if not topic_meta:
                not_found.append(topic_id)
                continue

            doc_url = f"{base_url}{topic_meta.get('path')}"
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

        result = {
            "status": "success" if results else "error",
            "message": f"Retrieved {len(results)} documentation topic(s)",
            "requested": topic_ids,
            "not_found": not_found if not_found else None,
            "documentation": results
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error fetching documentation: {str(e)}"
        }, indent=2)


async def get_project_setup():
    """Workflow tool wrapper for project-setup."""
    return await get_documentation("project-setup")


async def get_implementation_checklist():
    """Workflow tool wrapper for implementation-checklist."""
    return await get_documentation("implementation-checklist")


async def get_dev_workflow():
    """Workflow tool wrapper for dev-workflow."""
    return await get_documentation("dev-workflow")


async def get_architecture_patterns():
    """Workflow tool wrapper for architecture-patterns."""
    return await get_documentation("architecture-patterns")


async def get_common_pitfalls():
    """Workflow tool wrapper for common-pitfalls."""
    return await get_documentation("common-pitfalls")


async def test_get_project_setup():
    """Test 1: get_project_setup"""
    print("=" * 80)
    print("TEST 1: get_project_setup")
    print("=" * 80)

    result = await get_project_setup()
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")

    if result_data.get('documentation'):
        doc = result_data['documentation'][0]
        print(f"Topic: {doc.get('topic_id')}")
        print(f"Title: {doc.get('title')}")
        print(f"Priority: {doc.get('priority')}")
        print(f"Content Length: {len(doc.get('content', ''))} characters")

    assert result_data.get('status') == 'success', "Failed to fetch project-setup"
    assert result_data['documentation'][0]['topic_id'] == 'project-setup'

    print("✅ Test 1 PASSED\n")
    return result_data


async def test_get_implementation_checklist():
    """Test 2: get_implementation_checklist"""
    print("=" * 80)
    print("TEST 2: get_implementation_checklist")
    print("=" * 80)

    result = await get_implementation_checklist()
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")

    if result_data.get('documentation'):
        doc = result_data['documentation'][0]
        print(f"Topic: {doc.get('topic_id')}")
        print(f"Title: {doc.get('title')}")
        print(f"Content Length: {len(doc.get('content', ''))} characters")

    assert result_data.get('status') == 'success', "Failed to fetch implementation-checklist"
    assert result_data['documentation'][0]['topic_id'] == 'implementation-checklist'

    print("✅ Test 2 PASSED\n")
    return result_data


async def test_get_dev_workflow():
    """Test 3: get_dev_workflow"""
    print("=" * 80)
    print("TEST 3: get_dev_workflow")
    print("=" * 80)

    result = await get_dev_workflow()
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")

    if result_data.get('documentation'):
        doc = result_data['documentation'][0]
        print(f"Topic: {doc.get('topic_id')}")
        print(f"Title: {doc.get('title')}")
        print(f"Content Length: {len(doc.get('content', ''))} characters")

    assert result_data.get('status') == 'success', "Failed to fetch dev-workflow"
    assert result_data['documentation'][0]['topic_id'] == 'dev-workflow'

    print("✅ Test 3 PASSED\n")
    return result_data


async def test_get_architecture_patterns():
    """Test 4: get_architecture_patterns"""
    print("=" * 80)
    print("TEST 4: get_architecture_patterns")
    print("=" * 80)

    result = await get_architecture_patterns()
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")

    if result_data.get('documentation'):
        doc = result_data['documentation'][0]
        print(f"Topic: {doc.get('topic_id')}")
        print(f"Title: {doc.get('title')}")
        print(f"Content Length: {len(doc.get('content', ''))} characters")

    assert result_data.get('status') == 'success', "Failed to fetch architecture-patterns"
    assert result_data['documentation'][0]['topic_id'] == 'architecture-patterns'

    print("✅ Test 4 PASSED\n")
    return result_data


async def test_get_common_pitfalls():
    """Test 5: get_common_pitfalls"""
    print("=" * 80)
    print("TEST 5: get_common_pitfalls")
    print("=" * 80)

    result = await get_common_pitfalls()
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")

    if result_data.get('documentation'):
        doc = result_data['documentation'][0]
        print(f"Topic: {doc.get('topic_id')}")
        print(f"Title: {doc.get('title')}")
        print(f"Content Length: {len(doc.get('content', ''))} characters")

    assert result_data.get('status') == 'success', "Failed to fetch common-pitfalls"
    assert result_data['documentation'][0]['topic_id'] == 'common-pitfalls'

    print("✅ Test 5 PASSED\n")
    return result_data


async def main():
    """Run all workflow tool tests."""
    print("\n" + "=" * 80)
    print("🧪 TESTING WORKFLOW-SPECIFIC DOCUMENTATION TOOLS")
    print("=" * 80 + "\n")

    try:
        # Test all 5 workflow tools
        await test_get_project_setup()
        await test_get_implementation_checklist()
        await test_get_dev_workflow()
        await test_get_architecture_patterns()
        await test_get_common_pitfalls()

        print("=" * 80)
        print("✅ ALL WORKFLOW TOOLS TESTS PASSED SUCCESSFULLY!")
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
