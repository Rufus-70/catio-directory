# Step 4: Website Verification (Crawl4AI + Claude Code)

## Goal
Visit every business website and verify they actually build catios (not just general contractors or pet stores).

**Input**: Cleaned CSV (~500-3,000 businesses)
**Output**: Verified CSV (~300-500 actual catio builders)
**Time**: 2-6 hours (runs overnight)

---

## Claude Code Prompt for Verification Script

### Copy this into Claude Code:

```
I need to verify which businesses from my cleaned CSV actually build catios.

File: ~/catio-directory/data/cleaned/catio-builders-cleaned-YYYY-MM-DD.csv

Please create a Python script that:

1. SETUP:
   - Imports AsyncWebCrawler from crawl4ai
   - Loads the CSV with pandas
   - Filters to only businesses that have a website

2. CRAWL LOGIC:
   - For each business website:
     a. Use AsyncWebCrawler to fetch the page content
     b. Look for catio-related keywords in the text
     c. Assign a confidence score (high/medium/low/none)
   
3. CATIO KEYWORDS TO SEARCH FOR:
   Primary (strong signals):
   - "catio"
   - "cat enclosure"
   - "cat patio"
   - "outdoor cat habitat"
   - "cat tunnel"
   - "cat run"
   
   Secondary (medium signals):
   - "custom pet enclosures" + "cat"
   - "feline outdoor space"
   - "cat-safe outdoor"
   - "screened cat area"
   
   Context clues (weak signals):
   - "pet enclosure" + "screen" + "outdoor"
   - "custom animal habitat"

4. CONFIDENCE SCORING:
   - HIGH: Found 2+ primary keywords OR 1 primary + 2 secondary
   - MEDIUM: Found 1 primary keyword OR 3+ secondary keywords
   - LOW: Found 2 secondary keywords OR multiple context clues
   - NONE: No relevant keywords found

5. ERROR HANDLING:
   - Skip websites that timeout (>30 seconds)
   - Skip websites that return 404/500 errors
   - Skip websites that block crawlers (403/429)
   - Log all errors to ~/catio-directory/logs/verification-errors.log

6. PERFORMANCE:
   - Use async to crawl 10 websites concurrently
   - Save progress every 50 websites to ~/catio-directory/data/verified/partial-results.csv
   - Show progress bar (current site / total sites)

7. OUTPUT:
   Create ~/catio-directory/data/verified/catio-builders-verified-YYYY-MM-DD.csv with columns:
   - All original columns from input CSV
   - verification_status (high/medium/low/none/error)
   - keywords_found (list of matched keywords)
   - crawled_at (timestamp)
   - error_message (if failed)

8. SUMMARY REPORT:
   After completion, print:
   - Total businesses processed
   - High confidence: X (%)
   - Medium confidence: X (%)
   - Low confidence: X (%)
   - No match: X (%)
   - Errors: X (%)
   - Top 10 most common error messages

Before you write the script, please:
1. Check if Crawl4AI is installed correctly
2. Show me your game plan
3. Ask if I want to adjust any parameters (concurrency, timeout, keywords, etc.)
```

---

## Expected Conversation with Claude Code

Claude Code will probably ask:
1. "Should I include cat-related keywords like 'outdoor cat safety' or stick to catio-specific?"
   → **Answer**: Include them as secondary keywords

2. "How aggressive should the filtering be? Should I mark 'low confidence' as potential matches?"
   → **Answer**: Yes, keep low confidence. We'll manually review those later.

3. "Do you want me to extract other data while crawling (pricing, service areas, etc.)?"
   → **Answer**: No, let's verify first, enrich data in later steps.

---

## Running the Verification Script

Once Claude Code creates `verify_catio_builders.py`:

```bash
cd ~/catio-directory/scripts/
python3 verify_catio_builders.py
```

**Expected runtime**:
- 500 websites × 3 seconds average = ~25 minutes
- 3,000 websites × 3 seconds average = ~2.5 hours

**Pro tip**: Run it in a `tmux` session so it continues if you disconnect:
```bash
tmux new -s catio-verify
python3 verify_catio_builders.py
# Detach: Ctrl+B, then D
# Reattach later: tmux attach -t catio-verify
```

---

## Reviewing Results

After the script finishes, use Claude Code to analyze results:

```
Please analyze ~/catio-directory/data/verified/catio-builders-verified-YYYY-MM-DD.csv and show me:

1. Count by verification_status
2. Geographic distribution (state/province) of HIGH confidence matches
3. Random sample of 10 HIGH confidence businesses (names + websites)
4. Random sample of 5 MEDIUM confidence businesses (to spot-check)
5. Random sample of 5 LOW confidence businesses (to spot-check)
6. Most common keywords_found

Based on the results, should we:
- Adjust the keyword list?
- Re-crawl the MEDIUM/LOW confidence businesses with different logic?
- Mark some categories for manual review?
```

---

## Quality Check

### Good Signs:
- 30-50% of cleaned businesses marked as HIGH confidence
- Keyword matches make sense (not false positives)
- Geographic distribution looks reasonable (more in urban areas)

### Bad Signs (need adjustment):
- <10% HIGH confidence → Keywords too strict, relax scoring
- >80% HIGH confidence → Keywords too loose, seeing false positives
- Many "cat" + "enclosure" but not catio-specific → Add exclusion keywords

### Exclusion Keywords to Add (if needed):
- "dog enclosure" (unless also mentions cats)
- "chicken coop"
- "rabbit hutch"
- "aviary"

---

## Expected Results

### Phase 1 (Pacific Northwest)
- Cleaned businesses: ~500
- After verification:
  - HIGH confidence: ~150-200 (30-40%)
  - MEDIUM confidence: ~100-150 (20-30%)
  - LOW confidence: ~50-100 (10-20%)
  - NO MATCH: ~100-150 (20-30%)

### Nationwide
- Cleaned businesses: ~3,000
- After verification:
  - HIGH confidence: ~700-1,000
  - MEDIUM confidence: ~500-700
  - LOW confidence: ~300-500
  - NO MATCH: ~500-800

---

## Manual Review (Optional)

For MEDIUM/LOW confidence businesses, you can manually spot-check:

```bash
# Extract MEDIUM confidence with websites
python3 << 'EOF'
import pandas as pd

df = pd.read_csv('~/catio-directory/data/verified/catio-builders-verified-YYYY-MM-DD.csv')
medium = df[df['verification_status'] == 'medium'][['name', 'website', 'keywords_found']]

print(medium.head(20))
EOF
```

Visit a few websites and see if the verification logic is accurate.

---

## Next Steps

**If verification looks good (30-50% HIGH confidence)**:
→ Move to **Step 5: Data Enrichment (Catio Types)**

**If verification needs tuning**:
→ Adjust keywords/scoring and re-run
→ Use Claude Code to refine the logic

---

## Frey's Pro Tip

> "I ran this 2-3 times until pretty much all of my data was good. Don't expect perfection on the first pass."

**Expect to iterate**:
- Run 1: Too strict → Only 10% match → Relax keywords
- Run 2: Too loose → 80% match → Add exclusion rules
- Run 3: Just right → 30-40% match → Ready for enrichment

---

## Troubleshooting

### "Script crashes after 50 websites"
- Memory leak in AsyncWebCrawler
- Solution: Restart crawler every 100 sites

### "Too many timeouts"
- Increase timeout from 30s to 60s
- Reduce concurrency from 10 to 5

### "IP getting blocked"
- Add random delays between requests (0.5-2 seconds)
- Use rotating user agents
- Spread crawling over 2-3 days

---

## Save Your Work

```bash
# Backup verified data
cp ~/catio-directory/data/verified/catio-builders-verified-*.csv \
   ~/catio-directory/data/verified/backup-$(date +%Y%m%d).csv

# Commit to git
cd ~/catio-directory
git add .
git commit -m "Step 4 complete: Website verification finished"
git push
```
