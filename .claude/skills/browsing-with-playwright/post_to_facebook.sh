#!/bin/bash
cd "E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright"

# Click the post button
echo "Clicking post button..."
python scripts/mcp-client.py call --url http://localhost:8808 --tool browser_click --params '{"element":"post button","ref":"e408"}'

sleep 3

# Get snapshot to find text area
echo "Getting snapshot..."
python scripts/mcp-client.py call --url http://localhost:8808 --tool browser_snapshot --params '{}' > snapshot.txt

# Find the text area ref from snapshot
echo "Looking for text area..."
grep -i "textbox\|textarea" snapshot.txt | head -5

echo "Done"
