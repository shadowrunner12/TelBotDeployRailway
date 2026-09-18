# Railway VPN Panel Deploy Bot

A Telegram bot that deploys the [vless-panel](../vless-panel) project onto your
own Railway accounts, and manages the results — up to 2 panels per account,
password rotation, redeploys, and a 24h health sweep.

Only responds to one Telegram user ID (`OWNER_TELEGRAM_ID`) — everyone else is
silently ignored.

## 1. Create the Telegram bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` →
   follow the prompts → copy the token it gives you.
2. Message [@userinfobot](https://t.me/userinfobot) to get your own numeric
   Telegram user ID.

## 2. Generate an encryption key

Railway account tokens are encrypted at rest with this key. Run locally:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Save the output — you'll set it as `ENCRYPTION_KEY`. **Keep the same key on
every future redeploy of this bot**, or old backups/data won't decrypt.

## 3. Push this repo to GitHub

```bash
cd railway-vpn-bot
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/<you>/railway-vpn-bot.git
git push -u origin main
```

## 4. Deploy the bot itself on Railway

1. Railway → **New Project → Deploy from GitHub repo** → pick this repo.
   Railway reads the `Procfile` (`worker: python bot.py`) automatically —
   this is a background worker, it doesn't need a public domain.
2. Service → **Variables** → add:
   - `TELEGRAM_BOT_TOKEN` — from step 1
   - `OWNER_TELEGRAM_ID` — from step 1
   - `TARGET_REPO` — the GitHub repo of the *panel* project, e.g.
     `yourname/vless-panel` (this is what gets deployed when you tap
     "Deploy Panel" in the bot — push that project to its own repo first
     if you haven't)
   - `ENCRYPTION_KEY` — from step 2
   - Optional: `MAX_PANELS_PER_ACCOUNT` (default `2`),
     `HEALTH_SWEEP_INTERVAL_HOURS` (default `24`)
3. Deploy. Check **Logs** for `bot starting (polling)`.
4. Message your bot `/start` on Telegram.

## 5. Add a Railway account to the bot

You'll need an **account-level** API token (not a project token) so the bot
can create new projects on your behalf:
[railway.com/account/tokens](https://railway.com/account/tokens) → create
token → copy it.

In the bot: `/start` → `👤 Accounts` → `➕ Add Account` → paste the token →
give it a label. The bot validates it live before saving.

## 6. Deploy a panel

`/start` → `🚀 Deploy Panel` → pick the account → pick a region → wait. You'll
get back the panel's login URL and its admin password when it finishes,
tap-to-copy in Telegram. Progress is shown live in the same message as it
moves through each step.

Each deploy also attaches a 0.5GB volume to the panel automatically and
points its `DB_PATH` at it, so the panel's own data survives redeploys —
this closes the ephemeral-disk gap the panel project's README warned about.
If your account is already at its volume limit, the deploy still succeeds
but tells you storage wasn't attached.

## Notes

- **Bot data persistence**: attach a volume to the *bot's own* Railway
  service (Settings → Volumes, any mount path) and it's picked up
  automatically — no env var needed, since Railway sets
  `RAILWAY_VOLUME_MOUNT_PATH` for you and the bot checks for it. Without a
  volume, `bot.db` sits on ephemeral disk and can be wiped on redeploy;
  use `💾 Backup / Import` as a second line of defense either way.
- **Region selection**: Railway's own docs list per-service region choice
  as a Pro-plan feature. The bot still sends the request on every deploy
  since it's harmless to try — on a Free/Trial account it may simply be
  ignored and the panel deploys to Railway's default region instead.
- **Health sweep**: runs every `HEALTH_SWEEP_INTERVAL_HOURS` (default 24h)
  and only messages you when a panel's or account's status *changes* —
  not on every sweep — so it won't spam you while something stays down.
  Mute alerts for a specific panel from its detail view if you don't want
  it checked at all.
- **Account deletion**: if the account still has panels, you're asked
  whether to delete those panels' Railway projects too, or just remove the
  account from the bot and leave them running.
- **Workspace ID**: Railway currently requires a Workspace ID to create
  new projects on most accounts, with no reliable way for the bot to look
  it up on its own — that's a Railway platform limitation as of writing,
  not something this bot can smooth over further. Get yours once via
  Ctrl/Cmd+K → "Copy Active Workspace ID" in the dashboard.
