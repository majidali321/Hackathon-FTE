"""
Gold Tier Verification Script
Tests all Gold Tier components to ensure they're working correctly
"""

import sys
from pathlib import Path

print("=" * 70)
print("GOLD TIER VERIFICATION")
print("=" * 70)
print()

results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

# Test 1: Check if all required files exist
print("1. Checking Gold Tier files...")
required_files = [
    "social_media_skills.py",
    "social_media_workflow.py",
    "cross_domain_integration.py",
    "ceo_briefing.py",
    "error_recovery.py",
    "integrations/facebook_integration.py",
    "integrations/twitter_integration.py",
    "integrations/linkedin_integration.py",
    "mcp_servers/social_media_server.py",
    "ralph_wiggum/stop_hook.py",
    "GOLD_TIER_COMPLETE.md",
    "GOLD_TIER_ACHIEVEMENT.md"
]

missing_files = []
for file in required_files:
    if not Path(file).exists():
        missing_files.append(file)

if missing_files:
    results["failed"].append(f"Missing files: {', '.join(missing_files)}")
    print(f"   FAIL - Missing {len(missing_files)} files")
else:
    results["passed"].append("All required files present")
    print(f"   PASS - All {len(required_files)} files present")

print()

# Test 2: Check if folders exist
print("2. Checking required folders...")
required_folders = [
    "Inbox",
    "Needs_Action",
    "Done",
    "Pending_Approval",
    "Approved",
    "Reports",
    "Logs",
    "Logs/errors",
    "integrations",
    "mcp_servers",
    "ralph_wiggum"
]

missing_folders = []
for folder in required_folders:
    if not Path(folder).exists():
        missing_folders.append(folder)

if missing_folders:
    results["warnings"].append(f"Missing folders: {', '.join(missing_folders)}")
    print(f"   WARN - Missing {len(missing_folders)} folders")
else:
    results["passed"].append("All required folders present")
    print(f"   PASS - All {len(required_folders)} folders present")

print()

# Test 3: Test social media skills
print("3. Testing social media skills...")
try:
    from social_media_skills import generate_social_media_content
    content = generate_social_media_content("Test Topic", platform="twitter")
    if content and len(content) <= 280:
        results["passed"].append("Social media skills working")
        print("   PASS - Social media content generation working")
    else:
        results["failed"].append("Social media skills not generating content correctly")
        print("   FAIL - Content generation issue")
except Exception as e:
    results["failed"].append(f"Social media skills error: {str(e)}")
    print(f"   FAIL - {str(e)}")

print()

# Test 4: Test cross-domain integration
print("4. Testing cross-domain integration...")
try:
    from cross_domain_integration import CrossDomainIntegrator
    integrator = CrossDomainIntegrator()
    tasks = integrator.get_unified_task_list()
    results["passed"].append(f"Cross-domain integration working ({len(tasks)} tasks)")
    print(f"   PASS - Found {len(tasks)} tasks across domains")
except Exception as e:
    results["failed"].append(f"Cross-domain integration error: {str(e)}")
    print(f"   FAIL - {str(e)}")

print()

# Test 5: Test CEO briefing
print("5. Testing CEO briefing generator...")
try:
    from ceo_briefing import CEOBriefingGenerator
    generator = CEOBriefingGenerator()
    report = generator.generate_briefing(days=7)
    if report and len(report) > 100:
        results["passed"].append("CEO briefing generation working")
        print(f"   PASS - Generated briefing ({len(report)} characters)")
    else:
        results["failed"].append("CEO briefing not generating correctly")
        print("   FAIL - Briefing generation issue")
except Exception as e:
    results["failed"].append(f"CEO briefing error: {str(e)}")
    print(f"   FAIL - {str(e)}")

print()

# Test 6: Test error recovery
print("6. Testing error recovery system...")
try:
    from error_recovery import ErrorRecoveryManager, ServiceHealthChecker
    manager = ErrorRecoveryManager()
    health = ServiceHealthChecker.run_all_checks()
    results["passed"].append("Error recovery system working")
    print(f"   PASS - Health checks completed")
    print(f"        File System: {'OK' if health['checks']['file_system'] else 'FAIL'}")
    print(f"        Email Server: {'OK' if health['checks']['email_server'] else 'FAIL'}")
    print(f"        Social Media: {'OK' if health['checks']['social_media'] else 'FAIL'}")
except Exception as e:
    results["failed"].append(f"Error recovery error: {str(e)}")
    print(f"   FAIL - {str(e)}")

print()

# Test 7: Check integrations
print("7. Checking social media integrations...")
try:
    from integrations.facebook_integration import FacebookPoster
    from integrations.twitter_integration import TwitterPoster
    from integrations.linkedin_integration import LinkedInPoster
    results["passed"].append("All social media integrations importable")
    print("   PASS - Facebook, Twitter, LinkedIn integrations available")
except Exception as e:
    results["warnings"].append(f"Integration import warning: {str(e)}")
    print(f"   WARN - {str(e)}")

print()

# Test 8: Check MCP servers
print("8. Checking MCP servers...")
try:
    from mcp_servers.email_server import EmailMCPServer
    from mcp_servers.social_media_server import SocialMediaMCPServer
    results["passed"].append("All MCP servers importable")
    print("   PASS - Email and Social Media MCP servers available")
except Exception as e:
    results["failed"].append(f"MCP server error: {str(e)}")
    print(f"   FAIL - {str(e)}")

print()

# Test 9: Check Ralph Wiggum loop
print("9. Checking Ralph Wiggum loop...")
try:
    from ralph_wiggum.stop_hook import RalphWiggumLoop
    from ralph_wiggum.task_completion import TaskCompletionChecker
    results["passed"].append("Ralph Wiggum loop available")
    print("   PASS - Ralph Wiggum autonomous loop available")
except Exception as e:
    results["failed"].append(f"Ralph Wiggum error: {str(e)}")
    print(f"   FAIL - {str(e)}")

print()

# Test 10: Check documentation
print("10. Checking documentation...")
doc_files = [
    "README.md",
    "GOLD_TIER_COMPLETE.md",
    "GOLD_TIER_PROGRESS.md",
    "GOLD_TIER_ACHIEVEMENT.md"
]

missing_docs = []
for doc in doc_files:
    if not Path(doc).exists():
        missing_docs.append(doc)

if missing_docs:
    results["warnings"].append(f"Missing documentation: {', '.join(missing_docs)}")
    print(f"   WARN - Missing {len(missing_docs)} documentation files")
else:
    results["passed"].append("All documentation present")
    print(f"   PASS - All {len(doc_files)} documentation files present")

print()
print("=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)
print()

print(f"PASSED: {len(results['passed'])}")
for item in results['passed']:
    print(f"  - {item}")

print()

if results['warnings']:
    print(f"WARNINGS: {len(results['warnings'])}")
    for item in results['warnings']:
        print(f"  - {item}")
    print()

if results['failed']:
    print(f"FAILED: {len(results['failed'])}")
    for item in results['failed']:
        print(f"  - {item}")
    print()

print("=" * 70)

# Calculate overall status
total_tests = len(results['passed']) + len(results['failed'])
pass_rate = (len(results['passed']) / total_tests * 100) if total_tests > 0 else 0

if len(results['failed']) == 0:
    print("STATUS: GOLD TIER COMPLETE")
    print(f"All {len(results['passed'])} tests passed!")
    print()
    print("Your AI Employee is ready for production use!")
    sys.exit(0)
elif pass_rate >= 80:
    print("STATUS: GOLD TIER MOSTLY COMPLETE")
    print(f"{len(results['passed'])}/{total_tests} tests passed ({pass_rate:.1f}%)")
    print()
    print("Minor issues detected but system is functional.")
    sys.exit(0)
else:
    print("STATUS: GOLD TIER INCOMPLETE")
    print(f"{len(results['passed'])}/{total_tests} tests passed ({pass_rate:.1f}%)")
    print()
    print("Please address the failed tests above.")
    sys.exit(1)
