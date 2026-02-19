# DEPLOY CHECKLIST - TONIGHT

## ⚡ 30-SECOND DEPLOY (Recommended)

1. [ ] Open browser: https://app.netlify.com/drop
2. [ ] Drag `~/catio-directory/website` folder into browser window
3. [ ] Wait 10 seconds
4. [ ] Copy the live URL (https://something.netlify.app)
5. [ ] ✅ DONE - You have a live directory!

**Test it**:
- [ ] Visit the URL
- [ ] Portland Catios is featured at top
- [ ] Search box works (even if no results yet)
- [ ] Mobile responsive (check on phone)
- [ ] Share URL with your wife

---

## 🚀 2-HOUR FULL BUILD (If you want data tonight)

### Step 1: Scrape Data (10 min)

```bash
cd ~/catio-directory/scripts
python3 scrape_google_maps_FREE.py
```

**Checklist**:
- [ ] Created Apify account: https://apify.com/
- [ ] Got API token
- [ ] Ran scraper successfully
- [ ] CSV saved to `data/raw/`

### Step 2: Quick Clean (15 min)

```bash
# Open the CSV in your favorite tool
libreoffice ~/catio-directory/data/raw/*.csv

# Or use Excel/Google Sheets
```

**Remove**:
- [ ] Pet stores (PetSmart, Petco)
- [ ] Vets
- [ ] Closed businesses
- [ ] Obviously wrong entries

**Save to**: `data/cleaned/catio-builders-cleaned.csv`

### Step 3: Convert to Website Data (2 min)

```bash
cd ~/catio-directory/scripts
python3 csv_to_website_data.py ../data/cleaned/catio-builders-cleaned.csv
```

- [ ] JavaScript file created at `website/data/builders.js`

### Step 4: Update Website (5 min)

Edit `website/index.html`:

Find line ~200 (before `</body>`):

```html
<script>
    function searchBuilders() {
        const city = document.getElementById('citySearch').value;
        alert('Searching for catio builders in: ' + city);
    }
</script>
```

Replace with:

```html
<script src="data/builders.js"></script>
<script>
    function searchBuilders() {
        const city = document.getElementById('citySearch').value;
        const results = searchBuilders(city);
        
        if (results.length === 0) {
            alert('No builders found in: ' + city);
            return;
        }
        
        // Display results (simple version)
        alert(`Found ${results.length} builders in ${city}`);
        
        // TODO: Render results properly
    }
    
    // On page load, show actual city counts
    window.addEventListener('DOMContentLoaded', () => {
        const cityCards = document.querySelectorAll('#buildersList > div');
        const cityNames = ['Seattle, WA', 'Portland, OR', 'Vancouver, BC', 'Eugene, OR', 'Spokane, WA', 'Boise, ID'];
        
        cityCards.forEach((card, i) => {
            if (i < cityNames.length) {
                const [city, state] = cityNames[i].split(', ');
                const builders = getBuildersByCity(city, state);
                const countText = card.querySelector('p');
                if (countText && builders) {
                    countText.textContent = `${builders.length} verified catio builders`;
                }
            }
        });
    });
</script>
```

- [ ] Updated index.html

### Step 5: Deploy (30 sec)

```bash
cd ~/catio-directory/website
```

Drag folder to: https://app.netlify.com/drop

- [ ] Live at: https://something.netlify.app
- [ ] Real builder counts showing
- [ ] Search working (basic)

---

## 📋 POST-DEPLOY

### Immediately After Going Live

- [ ] Test on desktop browser
- [ ] Test on mobile browser
- [ ] Share URL with your wife
- [ ] Share in Portland Catios social media (if you have)
- [ ] Send to 2-3 friends for feedback

### Tomorrow Morning

- [ ] Submit to Google Search Console
- [ ] Create sitemap.xml
- [ ] Set up Google Analytics
- [ ] Check for any broken links

### This Week

- [ ] Install Crawl4AI
- [ ] Run automated verification
- [ ] Enrich data (catio types, materials)
- [ ] Add more cities (nationwide)

### This Month

- [ ] Register custom domain (catio-builders.com)
- [ ] Set up email (hello@catio-builders.com)
- [ ] Outreach to first 20 builders
- [ ] Create content pages (guides, comparisons)

---

## 🎉 SUCCESS METRICS

**Tonight (Deploy)**:
- ✅ Live URL exists
- ✅ Portland Catios prominently featured
- ✅ Site loads fast (<2 seconds)
- ✅ Mobile friendly
- ✅ Professional looking

**This Week (Growth)**:
- ✅ Google indexed (50+ pages)
- ✅ First 5 builders contacted
- ✅ 2-3 content pages published

**Month 1 (Traction)**:
- ✅ 100+ organic visitors
- ✅ 10+ cities with builder listings
- ✅ First inbound lead received

---

**Ready to deploy? Pick your path:**

- **Path A (30 sec)**: Deploy empty site now → https://app.netlify.com/drop
- **Path B (2 hrs)**: Follow steps above for full build

**LET'S GO** 🚀
