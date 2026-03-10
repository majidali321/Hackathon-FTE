import requests
import json
import time

def call_mcp(tool_name, arguments):
    response = requests.post(
        'http://localhost:8808/mcp',
        headers={
            'Accept': 'application/json, text/event-stream',
            'Content-Type': 'application/json'
        },
        json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        },
        stream=False
    )
    return response.text

# Step 1: Click the post button
print("Clicking post button...")
result = call_mcp("browser_click", {"element": "What's on your mind?", "ref": "e408"})
print(result)
time.sleep(2)

# Step 2: Get snapshot to find text input
print("\nGetting snapshot...")
result = call_mcp("browser_snapshot", {})
print(result[:500])

# Step 3: Type the message
print("\nTyping message...")
result = call_mcp("browser_type", {
    "element": "post text",
    "text": "ALHAMDULILLAH for Everything",
    "submit": False
})
print(result)
