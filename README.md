# Malee Distributor Match (v1)

**Live:** https://piyaster11.github.io/malee-distributor-match/

This is a two-way tool for Malee export sales:
- **Warm leads** come from real public posts where importers or distributors ask for juice, coconut water, canned fruit or OEM products, or publicly invite new brand partners. Each lead is tagged Product request, Partner seeking, OEM/private label or Other.
- **Push:** market fit per country, from UN Comtrade imports (HS 2009, 2202 and 2008), growth since 2021, Thailand's share, and FTA access.
- **Pull:** distributor need, an AI assessment based only on the evidence on the linked public page. Inputs the page doesn't show are marked "unknown" and never guessed.
- **Match** is the geometric mean of fit and need. Each match shows why it was made and which SKUs to pitch.
- **Also included:** a trip planner, CSV export, an "add a distributor" form (stored in localStorage), and an EN/TH toggle.

Details are company-level only, and no personal contact details are published. Need scores are discussion aids, not due diligence.

## Refresh (weekly is recommended)
Run these from the repo root:
1. `bash tools/sigfetch.sh` re-downloads the go4WorldBusiness and TradeKey buyer-request pages for the 8 markets into `data/sig/`.
2. Re-parse those pages into `data/sig/tk_keep.json` and `data/sig/g4_keep.json`. The parsing steps are inline in `tools/build_data.py`'s history; if the page markup changed, adjust the regexes.
3. Add hand-verified partner-seeking pages and new leads to the `M` list in `tools/build_data.py`. Each entry needs a source URL and a date.
4. `python3 tools/build_data.py` writes `docs/data.json`. Posts older than 12 months are marked stale.
5. Qualification: curl each lead's detail page into a folder outside the repo (it contains personal names, so don't commit it), run `python3 tools/profile.py <that folder>` to write the sanitized `data/profiles.json`, then run `python3 tools/qualify.py` to add requester type, size signals and the worth-the-effort rating, which is an AI assessment.
6. Optionally run `python3 tools/pull2.py` to refresh the Comtrade data, then commit and push.

GitHub Pages serves this repo from `docs/` on `main`.


## v2 additions (map, source types, trade-show / embassy sources)
- **Map** (Leaflet + OpenStreetMap tiles, no API key): country-level bubbles (buyer signals + distributors, colour = best worth-the-effort rating); click filters leads / match / trip. Positions are country centres (UAE/Saudi nudged apart).
- **Source types** on every signal and distributor: Buyer board, Company page, Trade show, Embassy-TTC, Directory. Filter in Leads and Match. `kind: route` marks offices/programmes that can match buyers (not buyers).
- New manual sources live in `tools/build_data.py` (`M2` list and the `X` distributor list, `DST` source types). Add the source URL, date (or `None` if undated), and keep company-level facts only. `tools/qualify.py` rates them (directory/trade-show/embassy evidence is capped at Medium unless the company invites new brands).
- Refresh: `python3 tools/build_data.py && python3 tools/qualify.py` from the repo root.
