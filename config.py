import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OWNER_TELEGRAM_ID = int(os.environ["OWNER_TELEGRAM_ID"])

# The GitHub repo Railway will deploy for each panel, e.g. "yourname/vless-panel"
TARGET_REPO = os.environ["TARGET_REPO"]
TARGET_BRANCH = os.environ.get("TARGET_BRANCH") or None

MAX_PANELS_PER_ACCOUNT = int(os.environ.get("MAX_PANELS_PER_ACCOUNT", "2"))
HEALTH_SWEEP_INTERVAL_HOURS = float(os.environ.get("HEALTH_SWEEP_INTERVAL_HOURS", "24"))

# Non-metal regions only (metal regions don't support volumes, and we attach one per panel).
# Region selection is listed by Railway as a Pro-plan feature — best-effort on Free/Trial.
REGIONS = [
    ("us-west1", "🇺🇸 US West (Oregon)"),
    ("us-east4", "🇺🇸 US East (Virginia)"),
    ("europe-west4", "🇳🇱 EU West (Amsterdam)"),
    ("asia-southeast1", "🇸🇬 Southeast Asia (Singapore)"),
]
