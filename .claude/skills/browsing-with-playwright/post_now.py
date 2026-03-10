import subprocess
import time

# Type the message
print("Typing message...")
result = subprocess.run([
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_type',
    '--params', '{"ref":"e1168","text":"ALHAMDULILLAH for Everything"}'
], capture_output=True, text=True, cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')
print(result.stdout)
print(result.stderr)

time.sleep(2)

# Get snapshot to find Post button
print("\nGetting snapshot...")
result = subprocess.run([
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_snapshot',
    '--params', '{}'
], capture_output=True, text=True, cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')
print(result.stdout[:1000])
