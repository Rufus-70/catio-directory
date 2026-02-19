# Step 1: OutScraper Setup & Data Collection

## What You Need
- OutScraper account: https://outscraper.com/
- $100 in credits (goes a long way - ~10,000 results = ~$30-50)

---

## Search Strategy

### Primary Keywords (Start Here)
1. **"custom catio builders"** - Most specific
2. **"catio installation"** - Service-focused
3. **"cat enclosure builders"** - Alternative term

### Secondary Keywords (If needed)
4. "outdoor cat habitat"
5. "custom pet enclosures"
6. "cat patio installation"

---

## Geographic Targeting (Phase 1: Pacific Northwest)

### Start Small, Then Expand
**Phase 1 (Week 1)**: Pacific Northwest
- Portland, OR
- Seattle, WA
- Vancouver, BC
- Eugene, OR
- Spokane, WA
- Boise, ID

**Phase 2 (Week 2)**: West Coast
- Los Angeles, CA
- San Francisco, CA
- San Diego, CA
- Sacramento, CA

**Phase 3 (Week 3)**: Nationwide expansion
- Denver, CO
- Austin, TX
- Minneapolis, MN
- Chicago, IL
- Boston, MA
- New York, NY
- Etc.

---

## OutScraper Configuration

### 1. Go to Google Maps Scraper
https://outscraper.com/google-maps-scraper/

### 2. Input Search Queries
Format: `[keyword] in [city, state]`

**Example queries for Phase 1**:
```
custom catio builders in Portland, OR
custom catio builders in Seattle, WA
catio installation in Portland, OR
catio installation in Seattle, WA
cat enclosure builders in Portland, OR
cat enclosure builders in Seattle, WA
```

**Pro tip**: OutScraper lets you upload a CSV of queries. Create a spreadsheet:
- Column A: Keywords
- Column B: Cities
- Combine in Column C: `=A1&" in "&B1`

### 3. Settings to Configure
- **Results per query**: 100-200 (most cities won't have more)
- **Extract emails**: YES (crucial for outreach later)
- **Extract website**: YES (needed for Crawl4AI)
- **Extract reviews**: NO (save credits, not needed)
- **Language**: English
- **Region**: US, CA (United States, Canada)

### 4. Output Format
- **CSV** (easiest to work with in Claude Code)
- Download all results into `/catio-directory/data/raw/`

---

## Expected Data Fields

OutScraper will give you:
- `name` - Business name
- `full_address` - Street address
- `city`
- `state`
- `postal_code`
- `country_code`
- `latitude`
- `longitude`
- `phone`
- `website`
- `domain`
- `business_status` - OPERATIONAL, CLOSED_PERMANENTLY, etc.
- `category` - Google Maps category
- `rating`
- `reviews`
- `price_level` - $, $$, $$$, $$$$

---

## Cost Estimate

**Phase 1 (Pacific Northwest)**:
- 6 cities × 3 keywords = 18 queries
- ~100 results per query = ~1,800 results
- Cost: ~$10-15

**Full Nationwide**:
- 50 major cities × 3 keywords = 150 queries
- ~100 results per query = ~15,000 results
- Cost: ~$50-75

**Recommendation**: Start with Phase 1 ($10-15), validate the workflow, then expand.

---

## File Naming Convention

Save downloaded CSVs as:
```
/catio-directory/data/raw/
  - outscraper_portland_custom-catio-builders_2026-02-18.csv
  - outscraper_seattle_custom-catio-builders_2026-02-18.csv
  - outscraper_portland_catio-installation_2026-02-18.csv
  - etc.
```

---

## Next Step
Once you have the raw CSVs, move to **Step 2: Data Cleaning with Claude Code**
