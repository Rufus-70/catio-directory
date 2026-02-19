# Step 5: Data Enrichment - Catio Types & Inventory

## Goal
Extract what types of catios each builder offers (window box, patio, standalone, tunnels, custom).

**Input**: Verified HIGH confidence businesses (~150-1,000)
**Output**: Enriched CSV with catio product inventory
**Time**: 1-3 hours
**Cost**: ~$20-30 in Claude API credits

---

## Why This Matters (Your Competitive Edge)

Most directories just list names and phone numbers.

**Your directory will show**:
- What types of catios they build
- Size ranges (small, medium, large, XL)
- Materials used (powder-coated aluminum, wood, PVC)
- Construction method (welded, bolted, DIY kits)
- Specializations (indoor/outdoor, multi-level, senior cats)

**This is the DATA MOAT Frey talks about.**

---

## Catio Types (Based on Portland Catios Expertise)

From your experience, catios fall into these categories:

### 1. **Window Box Catios**
- Attach to existing window
- Small footprint (3x3 to 4x6 feet)
- Typical price: $800-$2,500
- Use case: Apartments, condos, indoor cats

### 2. **Patio/Deck Catios** (Attached)
- Connect to house via door or cat door
- Medium to large (6x8 to 10x20 feet)
- Typical price: $3,000-$8,000
- Use case: Homeowners, multi-cat households

### 3. **Standalone Catios** (Freestanding)
- Separate structure in yard
- Size varies (8x8 to 16x20+ feet)
- Typical price: $4,000-$15,000+
- Use case: Large properties, multiple cats, show cats

### 4. **Cat Tunnels/Walkways**
- Connect house to catio or multiple catios
- Elevated or ground-level
- Typical price: $500-$2,000 per section
- Use case: Indoor/outdoor access, exercise

### 5. **Custom/Hybrid Designs**
- Multi-level, wraparound, integrated with landscaping
- Typical price: $10,000-$30,000+
- Use case: Luxury homes, cat enthusiasts, breeders

### 6. **DIY Kits**
- Prefab panels, customer assembles
- Typical price: $500-$3,000
- Use case: Budget-conscious, handy homeowners

---

## Claude Code Prompt for Inventory Enrichment

```
I need to extract catio product inventory from verified builder websites.

File: ~/catio-directory/data/verified/catio-builders-verified-YYYY-MM-DD.csv

Filter to only businesses with verification_status = 'high'

Please create a Python script that:

1. SETUP:
   - Use Crawl4AI AsyncWebCrawler
   - Load the verified CSV
   - Filter to HIGH confidence businesses only

2. CRAWL STRATEGY:
   For each business website:
   a. Look for pages like:
      - /products, /services, /catios, /gallery, /pricing
      - Navigate to product/service pages if linked from homepage
   b. Extract text content from these pages
   c. Search for catio type keywords (see below)

3. CATIO TYPE KEYWORDS:

   WINDOW BOX:
   - "window box catio"
   - "window catio"
   - "window perch"
   - "window enclosure"
   - "apartment catio"

   PATIO/ATTACHED:
   - "patio catio"
   - "attached catio"
   - "deck catio"
   - "door-attached"
   - "connected to house"

   STANDALONE:
   - "freestanding catio"
   - "standalone catio"
   - "backyard catio"
   - "ground-level enclosure"
   - "yard catio"

   TUNNEL/WALKWAY:
   - "cat tunnel"
   - "cat walkway"
   - "catio tunnel"
   - "elevated tunnel"
   - "cat bridge"

   CUSTOM:
   - "custom design"
   - "custom build"
   - "luxury catio"
   - "multi-level catio"
   - "wraparound catio"

   DIY KIT:
   - "DIY kit"
   - "self-install"
   - "modular catio"
   - "prefab catio"
   - "catio kit"

4. SIZE EXTRACTION:
   Look for dimension patterns:
   - "3x3", "4x6", "8x10", "10x16", etc.
   - "small" (under 6x6)
   - "medium" (6x6 to 10x10)
   - "large" (10x10 to 16x16)
   - "XL" or "extra large" (over 16x16)

5. MATERIAL EXTRACTION:
   Look for keywords:
   - "powder-coated aluminum"
   - "welded aluminum frame"
   - "cedar wood"
   - "redwood"
   - "PVC"
   - "galvanized steel"
   - "pet-resistant screen"
   - "weather-resistant"

6. CONSTRUCTION METHOD:
   - "welded construction"
   - "bolted assembly"
   - "DIY assembly"
   - "professional installation included"
   - "turnkey installation"

7. SPECIAL FEATURES (if found):
   - "multi-level"
   - "shelving"
   - "perches"
   - "insulated" or "4-season"
   - "weatherproof"
   - "senior cat friendly" (ramps, low entry)
   - "multiple cats"

8. OUTPUT COLUMNS:
   Add these to the CSV:
   - has_window_box (yes/no)
   - has_patio_attached (yes/no)
   - has_standalone (yes/no)
   - has_tunnel (yes/no)
   - has_custom (yes/no)
   - has_diy_kit (yes/no)
   - sizes_offered (comma-separated list)
   - materials (comma-separated list)
   - construction_method (welded/bolted/diy/unknown)
   - special_features (comma-separated list)
   - product_page_url (if found)

9. ERROR HANDLING:
   - Some builders won't have detailed product pages → Mark as "unknown"
   - Timeout = 30 seconds per website
   - Save progress every 25 businesses

10. SUMMARY REPORT:
    - Total businesses enriched
    - Most common catio types offered
    - Most common sizes
    - Most common materials
    - Businesses with pricing information (bonus if found)

Before starting, show me:
1. Your crawling strategy
2. Example of how you'll extract catio types
3. How you'll handle edge cases (vague product descriptions)
```

---

## Expected Conversation with Claude Code

Claude will likely ask:

**Q**: "Should I try to extract pricing if I see it?"
**A**: Yes, but don't make it required. Add optional column `pricing_found` (text field)

**Q**: "What if a builder only says 'custom catios' without specifying types?"
**A**: Mark as `has_custom = yes`, leave other types as `no`, note in `special_features = "custom only"`

**Q**: "Should I look at image alt text or just page text?"
**A**: Both! Image alt text often has good keywords like "8x10 standalone catio"

---

## Review Enriched Data

After script finishes:

```
Please analyze ~/catio-directory/data/enriched/catio-inventory-YYYY-MM-DD.csv:

1. Show me the top 5 builders by variety of offerings
2. Most common catio type (window box vs patio vs standalone)
3. How many builders offer DIY kits? (These could be affiliate opportunities)
4. Sample of 10 businesses with full inventory data
5. Sample of 5 businesses with limited data (need manual review)

Quality check:
- Are the catio types accurate based on the keywords found?
- Any false positives (e.g., marking "window" mentions as window box catios)?
- Do the sizes/materials make sense?
```

---

## Your Domain Expertise Advantage

**You know catio building better than scrapers:**

### Manual Enhancement (Optional)
For your top 50-100 verified builders, consider:
1. Visiting their websites personally
2. Adding quality notes only YOU would know:
   - "Uses cheap bolted frames (Portland Catios uses welded)"
   - "Offers 10-year warranty (industry standard is 5)"
   - "Specializes in senior cat accessibility"

This creates **unfair advantage** in your directory.

---

## Expected Results

### High-Detail Builders (~40%)
- All catio types listed
- Sizes documented
- Materials specified
- Product pages found

**Example**:
```
Name: Catio Spaces (Seattle)
has_patio_attached: yes
has_standalone: yes
has_tunnel: yes
has_custom: yes
sizes_offered: small, medium, large, XL
materials: powder-coated aluminum, cedar, pet-resistant screen
construction_method: welded
special_features: multi-level, weatherproof, professional installation
```

### Medium-Detail Builders (~40%)
- Some catio types identified
- Limited size/material info
- Generic service descriptions

### Low-Detail Builders (~20%)
- Only mentions "catio" or "cat enclosures"
- No specific product pages
- Needs manual review or outreach

---

## Iteration Tips (From Frey)

> "The first time I did this, it would miss some amenities and features here and there. This is the very casual prompt that I wrote. I want you to go and identify all of the best pages."

**Expect to refine**:
- Run 1: Misses some product pages → Add more URL patterns to check
- Run 2: False positives on "window" mentions → Add context requirements
- Run 3: Good quality data → Ready for next step

---

## Cost Estimate

**Claude API usage**:
- 200 businesses × ~2,000 tokens per website = ~400k tokens
- Cost: ~$20-30 (Claude Sonnet via API)

**Alternative**: Use Claude Code (included in $100/month subscription)
- Slower but free
- No token limits

---

## Next Step

Once you have enriched inventory data:
→ **Step 6: Image Extraction (Optional)**
→ **Step 7: Service Areas & Contact Enrichment**

---

## Save Your Work

```bash
cd ~/catio-directory
git add data/enriched/
git commit -m "Step 5 complete: Catio inventory enrichment"
git push
```
