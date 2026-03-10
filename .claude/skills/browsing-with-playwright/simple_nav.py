import subprocess
import time

# Navigate to Facebook
print("Step 1: Navigating to Facebook...")
proc = subprocess.Popen([
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_navigate',
    '--params', '{"url":"https://www.facebook.com"}'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
   cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

stdout, stderr = proc.communicate()
print(stdout[:300] if stdout else "No output")
print("Waiting for page load...")
time.sleep(5)

# Take screenshot
print("\nStep 2: Taking screenshot...")
proc = subprocess.Popen([
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_take_screenshot',
    '--params', '{"type":"png","fullPage":false}'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
   cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

stdout, stderr = proc.communicate()
print(stdout[:500] if stdout else "No output")

print("\nDone. Please check the browser window.")
