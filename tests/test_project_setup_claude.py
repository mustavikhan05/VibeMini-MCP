#!/usr/bin/env python3
"""
Test script for get_project_setup with CLAUDE.md template
Tests that the tool fetches both project-setup docs and CLAUDE.md template
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
    """
    Test version of get_project_setup that fetches CLAUDE.md template.
    """
    try:
        # Get project setup docs
        setup_docs = await get_documentation("project-setup")

        # Fetch CLAUDE.md template from GitHub
        claude_md_url = f"{DOCS_CONFIG['BASE_URL']}CLAUDE.md"
        async with httpx.AsyncClient() as client:
            claude_response = await client.get(claude_md_url, timeout=30.0)
            claude_response.raise_for_status()
            claude_content = claude_response.text

        # Parse setup_docs to add CLAUDE.md
        setup_data = json.loads(setup_docs)

        # Add CLAUDE.md to response
        setup_data["claude_md_template"] = {
            "filename": "CLAUDE.md",
            "content": claude_content,
            "instructions": "Create this file in your project root directory. This file guides AI agents on using the MCP server."
        }

        setup_data["message"] = "Retrieved project setup workflow and CLAUDE.md template"

        return json.dumps(setup_data, indent=2)

    except Exception as e:
        # Fallback to just project setup if CLAUDE.md fetch fails
        return await get_documentation("project-setup")


async def test_get_project_setup_with_claude():
    """Test get_project_setup returns CLAUDE.md template."""
    print("=" * 80)
    print("TEST: get_project_setup with CLAUDE.md template")
    print("=" * 80)

    result = await get_project_setup()
    result_data = json.loads(result)

    print(f"Status: {result_data.get('status')}")
    print(f"Message: {result_data.get('message')}")

    # Check for project setup documentation
    assert result_data.get('status') == 'success', "Failed to fetch project setup"
    assert 'documentation' in result_data, "Missing documentation field"

    doc = result_data['documentation'][0]
    print(f"\nProject Setup Doc:")
    print(f"  Topic: {doc.get('topic_id')}")
    print(f"  Title: {doc.get('title')}")
    print(f"  Content Length: {len(doc.get('content', ''))} characters")

    # Check for CLAUDE.md template
    assert 'claude_md_template' in result_data, "Missing CLAUDE.md template"

    template = result_data['claude_md_template']
    print(f"\nCLAUDE.md Template:")
    print(f"  Filename: {template.get('filename')}")
    print(f"  Content Length: {len(template.get('content', ''))} characters")
    print(f"  Instructions: {template.get('instructions')}")

    # Verify content
    assert template.get('filename') == 'CLAUDE.md', "Wrong filename"
    assert len(template.get('content', '')) > 0, "Empty CLAUDE.md content"
    assert 'Selise Blocks' in template.get('content', ''), "Missing expected content"

    print("\n✅ Test PASSED: get_project_setup returns both docs and CLAUDE.md template\n")
    return result_data


async def main():
    """Run the test."""
    print("\n" + "=" * 80)
    print("🧪 TESTING get_project_setup WITH CLAUDE.md TEMPLATE")
    print("=" * 80 + "\n")

    try:
        await test_get_project_setup_with_claude()

        print("=" * 80)
        print("✅ TEST PASSED SUCCESSFULLY!")
        print("=" * 80)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
