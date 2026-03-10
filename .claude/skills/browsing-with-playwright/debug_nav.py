import subprocess
import time

# Navigate to Facebook
print("Navigating to Facebook...")
proc = subprocess.Popen([
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_navigate',
    '--params', '{"url":"https://www.facebook.com"}'
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
   cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

stdout, stderr = proc.communicate()
print("STDOUT:", stdout[:500])
print("STDERR:", stderr[:500])
print("Return code:", proc.returncode)
