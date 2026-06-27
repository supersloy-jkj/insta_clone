# Instaclone — Instagram Clone (Django)

A full-featured Instagram-inspired social media web application built with Python/Django.

---

## ✅ Submission Checklist

| Requirement | Status |
|---|---|
| Complete Django source code | ✓ |
| All files required to run | ✓ |
| `requirements.txt` included | ✓ |
| Working deployment URL | ✓ See deployment section |
| Test credentials provided | ✓ See below |

---

## 🔑 Test Credentials

| Field | Value |
|---|---|
| **Username** | `demo` |
| **Password** | `Demo@1234` |
| **Admin panel** | `/admin/` (same credentials) |

These are created automatically when the app starts on Railway/Render.

---

## 🌟 Features

- **User auth** — Register, login/logout, custom profile with bio, avatar, website
- **Posts** — Upload multiple photos/videos per post, captions, delete, carousel view
- **Feed** — Paginated feed of posts from people you follow
- **Likes & comments** — AJAX like/unlike, threaded comment replies
- **Follow system** — Follow/unfollow, followers/following lists
- **Stories** — 24h auto-expiring stories, full-screen viewer with progress bars & tap navigation
- **Saved posts** — Bookmark posts to a private saved collection
- **Direct messages** — 1:1 conversations, image attachments, inbox with unread badges
- **Search** — Find users by username

---

## 🚀 Deploy to Railway (Recommended — Free)

Railway gives you a live URL in ~3 minutes.

### Step 1 — Push your code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/instaclone.git
git push -u origin main
```

### Step 2 — Deploy on Railway
1. Go to **https://railway.app** → sign up with GitHub (free)
2. Click **New Project → Deploy from GitHub repo** → select your repo
3. Click **Add a Service → Database → PostgreSQL** (adds a free PostgreSQL database)
4. Click on your **web service** → **Variables** tab → add these:

| Variable | Value |
|---|---|
| `SECRET_KEY` | Click "Generate" or paste any random 50-char string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://*.up.railway.app` |
| `DATABASE_URL` | Auto-filled by Railway when you add PostgreSQL |

5. Railway auto-deploys. In ~2 minutes you'll get a URL like:
   `https://instaclone-production.up.railway.app`

> The `Procfile` runs migrations + creates the demo user automatically on every deploy.

---

## 🌐 Alternative: Deploy to Render (Also Free)

1. Go to **https://render.com** → sign up with GitHub
2. Click **New → Web Service** → connect your repo
3. Set:
   - **Build command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input`
   - **Start command:** `gunicorn instagram_clone.wsgi:application`
4. Add **New → PostgreSQL** database, copy the **Internal Database URL**
5. Under **Environment Variables** on the web service, add same variables as Railway table above, plus:
   - `DATABASE_URL` → paste the Internal Database URL
   - `ALLOWED_HOSTS` → `.onrender.com`
   - `CSRF_TRUSTED_ORIGINS` → `https://*.onrender.com`
6. Click **Deploy** — your URL will be `https://instaclone.onrender.com`

> **Note:** Render free tier sleeps after 15 min of inactivity. First load may take 30s to wake up.

---

## 💻 Run Locally

```bash
# 1. Clone or extract the project
cd instagram_clone

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file for local settings
cp .env.example .env
# (no changes needed for local SQLite development)

# 5. Set up database
python manage.py migrate

# 6. Create demo user (or create your own superuser)
python manage.py create_demo_user
# OR: python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**
Admin: **http://127.0.0.1:8000/admin/**

---

## 🏗️ Project Structure

```
instagram_clone/
├── instagram_clone/          # Project config
│   ├── settings.py           #   Environment-aware settings
│   ├── urls.py               #   Root URL config
│   └── wsgi.py
├── users/                    # Auth, profiles, follow system
│   ├── management/commands/
│   │   └── create_demo_user.py   # Auto-creates test account on deploy
│   ├── models.py             #   Custom User + Follow
│   ├── views.py
│   └── urls.py
├── posts/                    # Posts, likes, comments, saved
│   ├── models.py             #   Post, PostMedia, Like, Comment, SavedPost
│   ├── views.py
│   └── urls.py
├── stories/                  # 24h auto-expiring stories
│   ├── models.py             #   Story, StoryView
│   ├── views.py
│   └── urls.py
├── messaging/                # Direct messages
│   ├── models.py             #   Conversation, Message
│   ├── views.py
│   └── urls.py
├── templates/                # HTML templates (base + per-app)
├── static/                   # CSS & JS
├── media/                    # User uploads (gitignored)
├── Procfile                  # Railway/Render start commands
├── render.yaml               # One-click Render config
├── runtime.txt               # Python version pin
├── requirements.txt
└── manage.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 / Django 4.2 |
| Database (local) | SQLite |
| Database (production) | PostgreSQL |
| Static files | WhiteNoise |
| Production server | Gunicorn |
| Frontend | Django Templates + Bootstrap 5 + vanilla JS |
| Fonts | Google Fonts (Grand Hotel) |
| Icons | Bootstrap Icons |

---

## ⚙️ Environment Variables Reference

| Variable | Required in prod | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | Django secret key — keep private |
| `DEBUG` | ✅ | Set to `False` in production |
| `ALLOWED_HOSTS` | ✅ | Comma-separated hostnames e.g. `.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | ✅ | Full origin URLs for CSRF e.g. `https://*.up.railway.app` |
| `DATABASE_URL` | ✅ | PostgreSQL connection string (auto-set by Railway/Render) |

