# DEPLOY TO CLOUDFLARE PAGES (5 Minutes)

## Option 1: GitHub Pages (FASTEST - 2 minutes)

```bash
cd ~/catio-directory
git remote add origin https://github.com/YOUR_USERNAME/catio-directory.git
git push -u origin master

# Then on GitHub:
# 1. Go to Settings → Pages
# 2. Source: master branch, /website folder
# 3. Save
# 4. Live at: https://YOUR_USERNAME.github.io/catio-directory/
```

## Option 2: Cloudflare Pages (5 minutes)

```bash
# 1. Create Cloudflare account (free): https://dash.cloudflare.com/sign-up

# 2. Install Wrangler CLI
npm install -g wrangler

# 3. Login
wrangler login

# 4. Deploy
cd ~/catio-directory/website
wrangler pages deploy . --project-name=catio-builders

# 5. Live at: https://catio-builders.pages.dev
```

## Option 3: Netlify Drop (EASIEST - 30 seconds)

```bash
# 1. Go to: https://app.netlify.com/drop
# 2. Drag ~/catio-directory/website folder into browser
# 3. Done! Live at: https://random-name.netlify.app
```

## Recommended: Option 3 for TONIGHT

Use Netlify Drop to get it live in 30 seconds, then migrate to custom domain later.

**After deploy**:
1. Test the live site
2. Update Portland Catios contact form
3. Share the URL
4. Start collecting data tomorrow
