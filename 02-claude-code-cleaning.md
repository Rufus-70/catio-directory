# Step 2: Data Cleaning with Claude Code

## Overview
This step removes obvious junk data before deep verification with Crawl4AI.

**Input**: Raw OutScraper CSVs (~1,800-15,000 rows)
**Output**: Cleaned CSV (~500-3,000 rows)
**Time**: 5-10 minutes
**Tool**: Claude Code

---

## Prompt 1: Initial Data Cleaning

### Copy this into Claude Code:

```
I have multiple CSV files from OutScraper containing potential catio builders scraped from Google Maps.

Files are located in: ~/catio-directory/data/raw/

Please perform the following cleaning operations and combine all CSVs into a single cleaned file:

CRITERIA FOR REMOVAL:
1. Missing critical fields:
   - No business name
   - No address OR city OR state
   - No phone AND no website

2. Business status:
   - Remove: business_status = "CLOSED_PERMANENTLY"
   - Remove: business_status = "CLOSED_TEMPORARILY"
   - Keep: business_status = "OPERATIONAL" or blank

3. Obvious non-catio businesses (remove these categories):
   - Pet stores (PetSmart, Petco, etc.)
   - Big box retailers (Home Depot, Lowe's, etc.)
   - Veterinary clinics
   - Pet grooming salons
   - General contractors (unless name/category mentions catio/enclosure)
   - Fencing companies (unless catio-specific)

4. Duplicates:
   - Remove exact duplicates (same name + same address)
   - Remove near-duplicates (same phone number, different locations = franchise/spam)

5. Data quality:
   - Remove listings where name = address (data scraping error)
   - Remove listings with placeholder phone numbers (000-000-0000, 111-111-1111)
   - Remove listings with obviously fake websites (google.com, facebook.com as primary domain)

KEEP THESE (even if uncertain):
- Any business with "catio", "cat enclosure", "cat patio" in name
- Pet services IF they mention custom building/installation
- General contractors IF website exists (we'll verify later with Crawl4AI)
- Fence/deck builders IF name suggests cat-related work

OUTPUT:
1. Create ~/catio-directory/data/cleaned/catio-builders-cleaned-YYYY-MM-DD.csv
2. Generate a cleaning report with:
   - Total rows before cleaning
   - Total rows after cleaning
   - Number removed per category
   - Top 20 removed business names (for spot-checking)

Before you start, tell me:
- How many CSV files you found
- Total rows to process
- Your game plan for cleaning
```

---

## Prompt 2: Verify Cleaning Results

After Claude Code finishes, review the report and run:

```
Please analyze ~/catio-directory/data/cleaned/catio-builders-cleaned-YYYY-MM-DD.csv and show me:

1. Random sample of 20 businesses (to spot-check quality)
2. Count by state/province (geographic distribution)
3. Businesses with websites vs without websites
4. Top 10 most common Google Maps categories
5. Any suspicious patterns (duplicate phone numbers, weird addresses, etc.)

If you notice any obvious junk that slipped through, please flag it and suggest additional cleaning criteria.
```

---

## Expected Results

### Before Cleaning (Phase 1 Pacific Northwest)
- Raw rows: ~1,800
- Expected quality: 60-70% junk (pet stores, general contractors, vets)

### After Cleaning
- Cleaned rows: ~500-600
- Expected quality: 30-40% actual catio builders, 60-70% need deep verification

### Nationwide
- Raw rows: ~15,000
- After cleaning: ~3,000-5,000

---

## Quality Check Questions

**Review the sample and ask yourself**:
1. Are there obvious pet stores that slipped through?
2. Are there general contractors with no catio indication?
3. Do the websites look real (not placeholder domains)?
4. Are there clusters of duplicates (same phone, different addresses)?

**If quality looks good**: Move to Step 3 (Crawl4AI installation)
**If quality is poor**: Refine the cleaning criteria and re-run

---

## Pro Tip: Save Your Prompts

Create a file `~/catio-directory/prompts/cleaning-prompt.md` with your refined prompt so you can:
1. Re-run cleaning with new data batches
2. Share the workflow with others
3. Remember what worked 6 months from now

---

## Troubleshooting

### "Claude Code can't find the CSV files"
Check the file paths:
```bash
ls -lh ~/catio-directory/data/raw/
```

### "Too many rows, Claude Code is slow"
Split into smaller batches:
```
Process files in batches of 3-5 at a time, then combine the cleaned results.
```

### "Claude Code removed too much data"
Relax the criteria:
- Don't require BOTH phone AND website (keep if either exists)
- Keep more general contractors (let Crawl4AI filter them out)

---

## Next Step
Once you have a cleaned CSV with 500-3,000 potential catio builders, move to **Step 3: Crawl4AI Installation**
