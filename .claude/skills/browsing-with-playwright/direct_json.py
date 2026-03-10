import subprocess
import json

# Create the JSON params
params = {"url": "https://www.facebook.com"}
params_json = json.dumps(params)

print("Params JSON:", params_json)

# Write to a temp file and use file redirection
with open('temp_params.txt', 'w') as f:
    f.write(params_json)

# Use the file as input
cmd = [
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_navigate',
    '--params', params_json
]

print("Running command...")
result = subprocess.run(cmd, capture_output=True, text=True,
                       cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

print("STDOUT:", result.stdout[:500])
print("STDERR:", result.stderr[:500])
print("Return code:", result.returncode)
