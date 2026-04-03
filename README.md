# Barry's Opportunity Cleaner

Deletes opportunities accidentally created by Barry's Senior Living import on **March 25, 2026** across 418 companies in the Modern Amenities Close CRM org.

---

## Setup (one time)

### 1. Add your Close API key as a secret

1. In this repo, go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `CLOSE_API_KEY`
4. Value: your Modern Amenities Close API key
5. Click **Add secret**

> ⚠️ Remember to rotate the API key in Close after the run is complete.

---

## Running

Go to **Actions → Delete Barry's Opportunities → Run workflow**

You'll see a dropdown:

| Option | What it does |
|---|---|
| `dry_run: true` | Safe preview — shows every opportunity that *would* be deleted. Nothing is removed. |
| `dry_run: false` | Live delete — permanently removes the opportunities. |

**Always run dry first.** Review the log artifact before running live.

---

## Reviewing results

After each run, click into the workflow run and download the **opportunity-deletion-log** artifact. It contains a full list of every opportunity found or deleted, organized by company.

---

## What it targets

- **418 Senior Living companies** from Barry's import CSV
- **Only** opportunities with `date_created` between `2026-03-25T00:00:00Z` and `2026-03-26T00:00:00Z`
- Nothing else on any lead is touched
