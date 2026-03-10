import subprocess

# Click Post button
result = subprocess.run([
    'python', 'scripts/mcp-client.py', 'call',
    '--url', 'http://localhost:8808',
    '--tool', 'browser_run_code',
    '--params', '{"code":"async (page) => { await page.getByRole(\'button\', { name: \'Post\' }).click(); return \'Clicked Post\'; }"}'
], capture_output=True, text=True, cwd=r'E:\AGents Pic\Hackathon FTE\.claude\skills\browsing-with-playwright')

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
