import subprocess
import sys

# Test what the script receives
cmd = [
    'python', '-c',
    'import sys; print("Args:", sys.argv)',
    '--params', '{"url": "https://www.facebook.com"}'
]

result = subprocess.run(cmd, capture_output=True, text=True)
print("Test output:", result.stdout)

# Now test the actual mcp-client
cmd2 = [
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_navigate',
    '--params', '{"url": "https://www.facebook.com"}'
]

print("\nActual command args:")
print(cmd2)

# Add debugging to see what's being received
import os
os.chdir(r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

# Modify the script temporarily to debug
print("\nRunning actual command...")
result = subprocess.run(cmd2, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
