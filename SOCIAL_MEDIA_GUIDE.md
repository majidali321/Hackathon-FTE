# AGents Social Media Posting Guide

## Quick Start

Your AI Employee can now post to **Twitter/X**, **Instagram**, and **Facebook**!

## Credentials Setup ✅

All credentials are configured in `credentials.json`:
- ✅ Twitter/X (username + password + API tokens)
- ✅ Instagram (username + password)
- ✅ Facebook (email + password)

## How to Post

### Option 1: Post to All Platforms at Once

```bash
python agents_social_media_poster.py --content "Your message here"
```

### Option 2: Post to Specific Platform

**Twitter/X:**
```bash
python agents_social_media_poster.py --platform twitter --content "Your tweet (max 280 chars)"
```

**Instagram:**
```bash
python agents_social_media_poster.py --platform instagram --content "Your caption" --image path/to/image.jpg
```
*Note: Instagram requires an image*

**Facebook:**
```bash
python agents_social_media_poster.py --platform facebook --content "Your post"
```

### Option 3: Use in Python Code

```python
from agents_social_media_poster import AGentsSocialMediaPoster

poster = AGentsSocialMediaPoster()

# Post to all platforms
poster.post_to_all("Your content here")

# Post to specific platform
poster.post_to_platform('twitter', "Your tweet")
poster.post_to_platform('instagram', "Caption", image_path="image.jpg")
poster.post_to_platform('facebook', "Your post")
```

## Test the Integration

Run the test script to verify all platforms:

```bash
python test_all_social_media.py
```

This will post a test message to all three platforms.

## Individual Platform Tests

**Test Twitter/X only:**
```bash
cd integrations
python twitter_integration.py
```

**Test Instagram only:**
```bash
cd integrations
python instagram_integration.py
```

**Test Facebook only:**
```bash
cd integrations
python facebook_integration.py
```

## Important Notes

1. **Instagram** requires an image to post. Text-only posts will fail.
2. **Twitter/X** has a 280 character limit.
3. All platforms use Selenium WebDriver (Chrome required).
4. First run will open browser windows (use `--headless` to hide).
5. Login may require 2FA verification on first use.

## Headless Mode

To run without showing browser windows:

```bash
python agents_social_media_poster.py --content "Message" --headless
```

## Files Created

- `integrations/twitter_integration.py` - Twitter/X posting
- `integrations/instagram_integration.py` - Instagram posting
- `integrations/facebook_integration.py` - Facebook posting
- `agents_social_media_poster.py` - Main interface
- `test_all_social_media.py` - Test all platforms
- `credentials.json` - All credentials (updated)

## Your Credentials

**Twitter/X:**
- Username: majidali13@rocketmail.com
- Password: jalilahmed18
- API tokens configured ✅

**Instagram:**
- Username: majidali13@rocketmail.com
- Password: Majid@34071

**Facebook:**
- Email: majidali13@rocketmail.com
- Password: Majid@34071

## Next Steps

1. Run `python test_all_social_media.py` to test everything
2. Use `agents_social_media_poster.py` for automated posting
3. Integrate with your AGents workflow for autonomous posting

🎉 Your AI Employee is ready to post on social media!
