import subprocess
import time
import os

os.chdir(r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

# Try with shell=True
print("Navigating to Facebook...")
cmd = 'python scripts/mcp-client.py call --url http://localhost:8808 --tool browser_navigate --params "{\\"url\\":\\"https://www.facebook.com\\"}"'
print("Command:", cmd)

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("STDOUT:", result.stdout[:500])
print("STDERR:", result.stderr[:500])
print("Return code:", result.returncode)
