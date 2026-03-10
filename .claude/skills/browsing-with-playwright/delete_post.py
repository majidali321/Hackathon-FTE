import requests
import json
import time

def call_mcp_tool(tool_name, arguments):
    """Call MCP tool via HTTP"""
    url = 'http://localhost:8808/mcp'
    headers = {
        'Accept': 'application/json, text/event-stream',
        'Content-Type': 'application/json'
    }

    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Step 1: Navigate to Facebook profile
print("Navigating to Facebook profile...")
result = call_mcp_tool("browser_navigate", {"url": "https://www.facebook.com/me"})
print(json.dumps(result, indent=2)[:500])
time.sleep(3)

# Step 2: Get snapshot to find the post
print("\nGetting page snapshot...")
result = call_mcp_tool("browser_snapshot", {})
snapshot_text = json.dumps(result)

# Save snapshot for analysis
with open('facebook_snapshot.txt', 'w', encoding='utf-8') as f:
    f.write(snapshot_text)

print("Snapshot saved. Looking for the post...")

# Check if post exists
if "ALHAMDULILLAH for Everything" in snapshot_text:
    print("Found the post!")
else:
    print("Post not found in current view")

print("\nSnapshot saved to facebook_snapshot.txt")
