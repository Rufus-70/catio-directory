# Custom Catio Builders Directory
## Project Overview

**Goal**: Build a nationwide directory of custom catio builders that ranks for local searches and generates qualified leads.

**Timeline**: 4-7 days to build, 6-12 months for SEO traffic

**Budget**: <$250
- $100 Claude Code Max subscription (already have)
- $100 OutScraper credits
- $50 Claude API credits for data enrichment

**Revenue Model**:
1. Lead generation (sell qualified leads to builders)
2. Featured listings (Portland Catios at top)
3. Affiliate partnerships (catio material suppliers)

---

## Frey's 7-Step Process (Adapted for Catios)

### Step 1: Scrape Google Maps Data
**Tool**: OutScraper (https://outscraper.com/)
**Search Queries**:
- "custom catio builders"
- "catio installation"
- "cat enclosure builders"
- "outdoor cat habitat"
- "custom pet enclosures"

**Geographic Scope**: Start with Pacific Northwest (Portland, Seattle, Vancouver BC), then expand nationwide

**Expected Raw Data**: ~5,000-10,000 potential businesses

---

### Step 2: Clean Obvious Junk Data (Claude Code)
**Remove**:
- No business name/address/city/state
- Permanently closed listings
- Big box retailers (PetSmart, Home Depot)
- Generic contractors (need catio-specific)

**Expected Result**: ~2,000-3,000 businesses after first cleaning

---

### Step 3: Deep Clean with Website Verification (Crawl4AI)
**Install Crawl4AI**: Open-source LLM-friendly web crawler
**Task**: Visit every website and verify they actually build catios (not just general contractors)

**Keywords to search for**:
- "catio", "cat enclosure", "cat patio", "outdoor cat habitat"
- "cat tunnel", "cat run", "feline enclosure"
- "custom pet structures"

**Expected Result**: ~300-500 verified catio builders nationwide

---

### Step 4: Enrich - Catio Types/Inventory
**Extract**:
- Window box catios
- Patio catios (attached to house)
- Standalone catios (freestanding)
- Cat tunnels/walkways
- Custom designs

**Quality indicators** (you know these from Portland Catios):
- Powder-coated aluminum frames
- Welded vs bolted construction
- Screen material quality (pet-resistant mesh)
- Weather-resistant features
- DIY kits vs full installation

---

### Step 5: Enrich - Images (Crawl4AI + Claude Vision)
**Scrape**: Top 3-5 images from each builder's website
**Claude Vision API**: Select best quality images showing finished catios

**Note**: Will need to contact builders for permission or use stock images initially

---

### Step 6: Enrich - Features/Amenities
**Extract from websites**:
- Shelving/perches
- Multiple levels
- Weatherproofing
- Insulation (4-season)
- Access doors (human + cat)
- Secure latches
- UV-resistant materials
- Warranty information

---

### Step 7: Enrich - Service Areas
**Extract**:
- Cities/regions served
- Travel radius from main location
- Multi-state coverage

---

## Data Enrichment Strategy (Your Competitive Edge)

**What makes YOUR directory better**:
1. **Price transparency**: You know typical costs ($2k-$15k+) - scrape pricing where available
2. **Quality indicators**: Welded vs bolted, materials used, warranty length
3. **Build process**: DIY kits, partial install, full turnkey
4. **Specializations**: Indoor/outdoor, tunnels, multi-cat households, senior cats

**Data moat**: Most directories just list names/phones. You'll have actual decision-making data.

---

## Monetization Plan

### Phase 1 (Months 1-6): Build Authority
- Feature Portland Catios prominently
- Capture overflow leads (people searching outside Portland)
- Build backlinks through outreach to builders

### Phase 2 (Months 6-12): Lead Generation
- Sell qualified leads to builders in non-competing markets
- $50-150 per qualified lead (standard for home improvement)
- Target: 10-20 leads/month = $500-$3,000/month

### Phase 3 (Year 2+): Vertical SaaS
- CRM for catio builders (like Parting.com did for funeral homes)
- Quote calculator tool
- Customer management
- Monthly subscription: $99-299/month

---

## SEO Strategy

**Target Keywords** (low competition, high intent):
- "custom catio builders [city name]"
- "catio installation near me"
- "outdoor cat enclosure contractors"
- "cat patio builders"

**Content Strategy**:
- City-specific landing pages (300-500 pages)
- Comparison guides (DIY vs professional)
- Cost guides by region
- Material quality guides (your expertise shines here)

**Local SEO Advantage**: Less competition than "bathroom contractors" or "senior living"

---

## Timeline

**Week 1**: Scrape + clean data
**Week 2**: Install Crawl4AI, verify catio builders
**Week 3**: Enrich data (types, features, service areas)
**Week 4**: Build directory (Claude Code + Supabase)
**Months 2-6**: SEO optimization, outreach to builders
**Months 6-12**: Traffic growth, lead generation starts

---

## Next Steps

1. Set up OutScraper account
2. Run initial scrapes for Pacific Northwest
3. Clean data with Claude Code
4. Install Crawl4AI locally
5. Build enrichment pipeline
