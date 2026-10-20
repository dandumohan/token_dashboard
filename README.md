# Mreports suite — how to maintain and publish

## What is where
```
config.js                    Supabase URL + anon key (edit here once; build.py copies it into every page)
src/main/Mindex_supabase.html    the main app
src/mreports/index.html          Mreports (Reports tab, after Acc)
src/nursery/index.html           Nursery Transactions (Nursery tab, before Planting)
build.py                     makes dist/ and dist-single/
netlify.toml                 tells Netlify to run build.py and publish dist/
CHANGELOG.md                 one line per change
dist/            (generated)  multi-file site
dist-single/     (generated)  one-file version
```
**Edit only files in `src/` and `config.js`.** Never edit `dist/` or `dist-single/`; they are rebuilt.

## Everyday update (about 2 minutes)
1. Edit the one page you are changing in `src/`.
2. Run `python3 build.py`.
3. Open `dist/index.html` locally to check it, then publish (below).
4. Add a line to `CHANGELOG.md`.

## Publish option A — multi-file site on Netlify (recommended)
Each page has its own address, so fixing Mreports redeploys only that change.
- **With GitHub (automatic):** put this folder in a GitHub repository, then in Netlify choose
  *Add new site → Import from Git*. Netlify reads `netlify.toml`, so no settings are needed.
  Every push goes live in about a minute. Pushing a branch gives a private preview link to test first.
- **Without GitHub (manual):** run `python3 build.py`, then drag the **`dist`** folder onto
  *app.netlify.com/drop*.

Inside the main app the two pages open as frames from `/mreports/` and `/nursery/` and share its login.
Opened directly (`yoursite.netlify.app/mreports/`) each page shows its own sign-in, so you can test or share one page alone.

## Publish option B — one file (offline, pen drive, email, any simple host)
Use **`dist-single/Mindex_supabase.html`**. Both pages are copied inside it, so it is one file to open or upload.
It still needs internet for the Supabase data and the CDN libraries. After every page edit you must run `build.py` again.

## Adding another page later
1. Create `src/<name>/index.html`. Put `<!--@@CONFIG@@-->` right after `<head>`.
2. In it, use the main app's connection when framed: `window.parent.__<NAME>__.sb()`, else create its own Supabase client from `window.APP_CONFIG`.
3. In the main app add the tab button, a screen with an `<iframe>`, and a loader like `loadMreportsFrame()`.
4. In `build.py`, add the page to the three places that mention `nursery`.

## Safety
- The anon key in `config.js` is public by design; **row-level security** protects the data.
- Never put the `service_role` key or a database password in any file here.
- If a page looks old on a phone, check the build time in the page footer / view-source (`<meta name="build">`).
