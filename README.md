# Volta Intelligence — Newspaper Edition

A static, mobile-friendly, newspaper-style public intelligence site. **No paid API keys** required for the base experience.

## Features
- Responsive Financial Times-inspired editorial layout and scrolling **company watchlist** (not live prices)
- RSS-driven coverage of Volta, customers, competitors, power, supply chain, delivery and finance
- Public podcast feed collection, source links, search, filters, and device-local bookmarks
- GitHub Actions scheduled collection three times a day; historical archive retained up to 30 days
- No fabricated stories or financial quotes; empty-state display until collection runs

## Publish with GitHub Pages
1. Create a **public** repository called `volta-intelligence` (never upload confidential material).
2. Upload all files and folders, including `.github/workflows/collect.yml`.
3. Repository **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**.
4. Under **Actions**, run **Update public intelligence** with `Run workflow` to populate the feed.
5. Open `https://YOUR_USERNAME.github.io/volta-intelligence/` after Pages deployment completes.

## Costs and caveats
- Free public RSS collection and GitHub Pages hosting subject to GitHub usage policies.
- Market ticker shows company symbols/names only. **It does not display live share prices.** Integrate a licensed/verified quote source before showing market values.
- Google News RSS may link via Google News redirects and feeds can fail or change. Individual collection errors are logged and old articles are retained.
- Keyword relevance is heuristic, not Claude-generated executive analysis. Automated AI writing requires an explicitly configured AI execution service and cost controls.
- This is an unofficial independent briefing based only on public information.

## Run locally
Run `python -m http.server 8000` from the repository root, then visit `http://localhost:8000/`. Run `python collect.py` to fetch new items. No Python packages required.

## Market prices (new)
The scheduled GitHub Action also runs `markets.py`. It fetches **daily/delayed** market quotes from the unofficial Yahoo Finance public chart endpoint, with Stooq daily closes as fallback for US-listed symbols. These sources may block requests, change formats, or have licensing restrictions. This is **not a guaranteed live market-data service**. Failed symbols display N/A; prior quotes retained on failure are explicitly marked stale. Do not use for trading decisions. No API key is needed. Quotes and their as-of timestamps are stored in `data/markets.json`.

To refresh immediately, open **Actions → Update public intelligence → Run workflow**. After the workflow succeeds, allow a few minutes for GitHub Pages deployment. GitHub Pages must be configured to deploy the default branch root (`/`).

## Expanded intelligence edition
The 12 editorial desks now cover Volta and partners, customers, competitors, technology supply chain, power and construction, bonds and credit, AI financial stability, realised AI returns, commissioning, research, policy, and executive signals. `risk.py` collects publicly accessible FRED historical observations (high-yield spreads, investment-grade spreads, US Treasury yields and VIX), with dates and source links. These are **market context**, not an automated financial stress score. FRED endpoints and public quote providers can change; unavailable values remain unavailable. No private information should be added to a public GitHub Pages repository.

**Not yet implemented:** Claude API-based editorial analysis, verified counterparty dependency graph, automated contradiction detection, project milestone modelling, and reliable institutional-grade bond/CDS feeds. These require source validation and, for AI analysis, an explicitly configured billing budget. Never put API secrets into browser JavaScript or public files.
