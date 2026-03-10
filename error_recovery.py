"""
Enhanced Error Recovery and Graceful Degradation Module
Provides system resilience and fault tolerance
Part of Gold Tier requirements for Hackathon FTE
"""

import json
import time
import logging
import traceback
from datetime import datetime
from pathlib import Path
from functools import wraps

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ErrorRecoveryManager:
    """Manages error recovery and graceful degradation"""

    def __init__(self):
        self.error_log_dir = Path("Logs/errors")
        self.error_log_dir.mkdir(parents=True, exist_ok=True)
        self.recovery_attempts = {}
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def log_error(self, error_type, error_message, context=None):
        """
        Log error with full context

        Args:
            error_type (str): Type of error
            error_message (str): Error message
            context (dict): Additional context
        """
        try:
            timestamp = datetime.now()
            error_id = f"{error_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}"

            error_data = {
                "error_id": error_id,
                "timestamp": timestamp.isoformat(),
                "type": error_type,
                "message": str(error_message),
                "context": context or {},
                "traceback": traceback.format_exc()
            }

            # Save to JSON file
            error_file = self.error_log_dir / f"{error_id}.json"
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_data, f, indent=2)

            # Also append to daily log
            daily_log = self.error_log_dir / f"errors_{timestamp.strftime('%Y%m%d')}.log"
            with open(daily_log, 'a', encoding='utf-8') as f:
                f.write(f"\n[{timestamp.isoformat()}] {error_type}: {error_message}\n")

            logger.error(f"Error logged: {error_id}")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")

    def retry_with_backoff(self, func, *args, **kwargs):
        """
        Retry function with exponential backoff

        Args:
            func: Function to retry
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Result of function or None if all retries failed
        """
        func_name = func.__name__
        attempt = 0

        while attempt < self.max_retries:
            try:
                result = func(*args, **kwargs)
                if attempt > 0:
                    logger.info(f"Success on retry {attempt} for {func_name}")
                return result

            except Exception as e:
                attempt += 1
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2 ** (attempt - 1))  # Exponential backoff
                    logger.warning(f"Attempt {attempt} failed for {func_name}: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries} attempts failed for {func_name}")
                    self.log_error(
                        error_type=f"retry_exhausted_{func_name}",
                        error_message=str(e),
                        context={"function": func_name, "attempts": attempt}
                    )
                    return None

    def safe_execute(self, func, fallback=None, *args, **kwargs):
        """
        Execute function with fallback on error

        Args:
            func: Function to execute
            fallback: Fallback function or value
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Result of function or fallback
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            self.log_error(
                error_type=f"safe_execute_{func.__name__}",
                error_message=str(e),
                context={"function": func.__name__}
            )

            if callable(fallback):
                logger.info(f"Executing fallback for {func.__name__}")
                try:
                    return fallback(*args, **kwargs)
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
                    return None
            else:
                return fallback

    def check_service_health(self, service_name, check_func):
        """
        Check if a service is healthy

        Args:
            service_name (str): Name of service
            check_func: Function to check service health

        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            result = check_func()
            logger.info(f"Service {service_name} is healthy")
            return True
        except Exception as e:
            logger.error(f"Service {service_name} is unhealthy: {e}")
            self.log_error(
                error_type=f"service_health_{service_name}",
                error_message=str(e),
                context={"service": service_name}
            )
            return False

    def get_error_statistics(self, days=7):
        """
        Get error statistics for the last N days

        Args:
            days (int): Number of days to analyze

        Returns:
            dict: Error statistics
        """
        try:
            stats = {
                "total_errors": 0,
                "by_type": {},
                "by_day": {},
                "recent_errors": []
            }

            # Read error log files
            for error_file in self.error_log_dir.glob("*.json"):
                try:
                    with open(error_file, 'r', encoding='utf-8') as f:
                        error_data = json.load(f)

                    # Count by type
                    error_type = error_data.get("type", "unknown")
                    stats["by_type"][error_type] = stats["by_type"].get(error_type, 0) + 1

                    # Count by day
                    timestamp = error_data.get("timestamp", "")
                    day = timestamp[:10] if timestamp else "unknown"
                    stats["by_day"][day] = stats["by_day"].get(day, 0) + 1

                    # Track recent errors
                    stats["recent_errors"].append({
                        "id": error_data.get("error_id"),
                        "type": error_type,
                        "message": error_data.get("message", "")[:100],
                        "timestamp": timestamp
                    })

                    stats["total_errors"] += 1

                except Exception as e:
                    logger.error(f"Error reading error file {error_file}: {e}")

            # Sort recent errors by timestamp
            stats["recent_errors"].sort(key=lambda x: x["timestamp"], reverse=True)
            stats["recent_errors"] = stats["recent_errors"][:10]  # Keep only 10 most recent

            return stats

        except Exception as e:
            logger.error(f"Error getting error statistics: {e}")
            return {}


# Decorator for automatic retry
def auto_retry(max_retries=3, delay=2):
    """
    Decorator for automatic retry with exponential backoff

    Args:
        max_retries (int): Maximum number of retries
        delay (int): Initial delay in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt < max_retries:
                        wait_time = delay * (2 ** (attempt - 1))
                        logger.warning(f"Retry {attempt}/{max_retries} for {func.__name__} in {wait_time}s: {e}")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All retries exhausted for {func.__name__}: {e}")
                        raise
        return wrapper
    return decorator


# Decorator for graceful degradation
def graceful_degradation(fallback_value=None):
    """
    Decorator for graceful degradation

    Args:
        fallback_value: Value to return on error
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}, using fallback: {e}")
                return fallback_value
        return wrapper
    return decorator


# Service health checks
class ServiceHealthChecker:
    """Checks health of various services"""

    @staticmethod
    def check_file_system():
        """Check if file system is accessible"""
        try:
            test_file = Path("Logs/.health_check")
            test_file.parent.mkdir(exist_ok=True)
            test_file.write_text(f"Health check: {datetime.now().isoformat()}")
            test_file.unlink()
            return True
        except Exception as e:
            logger.error(f"File system health check failed: {e}")
            return False

    @staticmethod
    def check_email_server():
        """Check if email server is accessible"""
        try:
            from mcp_servers.email_server import EmailMCPServer
            server = EmailMCPServer()
            return server.test_connection()
        except Exception as e:
            logger.error(f"Email server health check failed: {e}")
            return False

    @staticmethod
    def check_social_media_integrations():
        """Check if social media integrations are available"""
        try:
            from integrations.facebook_integration import FacebookPoster
            from integrations.twitter_integration import TwitterPoster
            return True
        except Exception as e:
            logger.error(f"Social media integration health check failed: {e}")
            return False

    @staticmethod
    def run_all_checks():
        """Run all health checks"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "file_system": ServiceHealthChecker.check_file_system(),
                "email_server": ServiceHealthChecker.check_email_server(),
                "social_media": ServiceHealthChecker.check_social_media_integrations()
            }
        }

        results["overall_health"] = all(results["checks"].values())

        return results


def generate_error_report():
    """Generate error report"""
    manager = ErrorRecoveryManager()
    stats = manager.get_error_statistics()

    report = f"""# Error Recovery Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Error Statistics

**Total Errors**: {stats.get('total_errors', 0)}

### Errors by Type
"""

    for error_type, count in sorted(stats.get('by_type', {}).items(), key=lambda x: x[1], reverse=True):
        report += f"- **{error_type}**: {count}\n"

    report += f"""
### Errors by Day
"""

    for day, count in sorted(stats.get('by_day', {}).items(), reverse=True):
        report += f"- **{day}**: {count}\n"

    report += f"""
---

## Recent Errors (Last 10)

"""

    for error in stats.get('recent_errors', []):
        report += f"""### {error['id']}
- **Type**: {error['type']}
- **Time**: {error['timestamp']}
- **Message**: {error['message']}

"""

    report += f"""---

## System Health

"""

    health = ServiceHealthChecker.run_all_checks()
    for check_name, status in health['checks'].items():
        emoji = "✅" if status else "❌"
        report += f"- {emoji} **{check_name.replace('_', ' ').title()}**: {'Healthy' if status else 'Unhealthy'}\n"

    report += f"""
**Overall Status**: {'🟢 HEALTHY' if health['overall_health'] else '🔴 UNHEALTHY'}

---

*Generated by Error Recovery Manager*
*Part of Gold Tier Implementation - Hackathon FTE*
"""

    return report


if __name__ == "__main__":
    print("=" * 60)
    print("Error Recovery System Test")
    print("=" * 60)
    print()

    # Test 1: Health checks
    print("1. Running health checks...")
    health = ServiceHealthChecker.run_all_checks()
    print(json.dumps(health, indent=2))
    print()

    # Test 2: Error statistics
    print("2. Getting error statistics...")
    manager = ErrorRecoveryManager()
    stats = manager.get_error_statistics()
    print(f"Total errors: {stats.get('total_errors', 0)}")
    print()

    # Test 3: Generate report
    print("3. Generating error report...")
    report = generate_error_report()

    report_file = Path("Reports/ERROR_REPORT.md")
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text(report, encoding='utf-8')

    print(f"Report saved to: {report_file}")
    print()
    print(report)
