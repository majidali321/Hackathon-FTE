import subprocess
import json

def run_mcp_command(tool, params_dict):
    """Run MCP command using mcp-client.py"""
    params_json = json.dumps(params_dict)

    result = subprocess.run([
        'python', 'scripts/mcp-client.py', 'call',
        '--url', 'http://localhost:8808',
        '--tool', tool,
        '--params', params_json
    ], capture_output=True, text=True, cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

    return result.stdout, result.stderr

# Navigate to Facebook
print("Navigating to Facebook profile...")
stdout, stderr = run_mcp_command('browser_navigate', {'url': 'https://www.facebook.com/me'})
print(stdout[:500])

# Wait a bit
import time
time.sleep(3)

# Get snapshot
print("\nGetting snapshot...")
stdout, stderr = run_mcp_command('browser_snapshot', {})

# Save and check
with open('fb_snapshot.txt', 'w', encoding='utf-8') as f:
    f.write(stdout)

if 'ALHAMDULILLAH for Everything' in stdout:
    print("Found the post! Now searching for delete button...")
else:
    print("Post not found. It may not have been published.")

print("Snapshot saved to fb_snapshot.txt")
