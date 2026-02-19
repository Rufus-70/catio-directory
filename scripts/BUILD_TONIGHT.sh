#!/bin/bash
#
# BUILD CATIO DIRECTORY TONIGHT - MASTER SCRIPT
# 
# This orchestrates the entire build process:
# 1. Scrape data (FREE via Apify)
# 2. Clean data (Claude Code)
# 3. Install Crawl4AI
# 4. Verify websites
# 5. Enrich data
# 6. Build directory
# 7. Deploy
#
# Estimated time: 4-6 hours
# Estimated cost: $0-50
#

set -e  # Exit on error

PROJECT_ROOT="$HOME/catio-directory"
DATA_DIR="$PROJECT_ROOT/data"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

echo "================================================================"
echo "CATIO DIRECTORY BUILDER - TONIGHT'S BUILD"
echo "================================================================"
echo
echo "This script will build your entire directory in one session."
echo "Estimated time: 4-6 hours"
echo "Estimated cost: \$0-50 (using free tools)"
echo
read -p "Ready to start? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

#
# PHASE 1: DATA SCRAPING (10-15 min)
#
echo
echo "================================================================"
echo "PHASE 1: DATA SCRAPING"
echo "================================================================"
echo
echo "Options:"
echo "  1. FREE scraper (Apify free tier - \$0, takes 5-10 min)"
echo "  2. Manual Chrome extension (Instant Data Scraper - \$0, takes 15-20 min)"
echo "  3. Skip (I already have CSV files in data/raw/)"
echo
read -p "Choose option (1/2/3): " -n 1 -r SCRAPE_OPTION
echo

case $SCRAPE_OPTION in
    1)
        echo "Starting FREE Apify scraper..."
        echo
        echo "SETUP REQUIRED:"
        echo "1. Create free Apify account: https://apify.com/"
        echo "2. Get API token: https://console.apify.com/account/integrations"
        echo
        read -p "Paste your Apify API token: " APIFY_TOKEN
        export APIFY_API_TOKEN="$APIFY_TOKEN"
        
        python3 "$SCRIPTS_DIR/scrape_google_maps_FREE.py"
        ;;
    2)
        echo "Manual scraping instructions:"
        echo
        echo "1. Install Instant Data Scraper: https://instantdatascraper.com/"
        echo "2. Search Google Maps: 'custom catio builders in Portland, OR'"
        echo "3. Click extension, extract data, save CSV to: $DATA_DIR/raw/"
        echo "4. Repeat for: Seattle, Vancouver, Eugene, Spokane, Boise"
        echo "5. Repeat for keywords: 'catio installation', 'cat enclosure builders'"
        echo
        read -p "Press ENTER when you've saved all CSVs to data/raw/ ..."
        ;;
    3)
        echo "Skipping scraping, using existing CSVs..."
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

# Verify we have data
CSV_COUNT=$(ls -1 "$DATA_DIR/raw/"*.csv 2>/dev/null | wc -l)
if [ "$CSV_COUNT" -eq 0 ]; then
    echo
    echo "❌ ERROR: No CSV files found in data/raw/"
    echo "Please add at least one CSV file before continuing."
    exit 1
fi

echo
echo "✅ Found $CSV_COUNT CSV file(s) in data/raw/"
echo

#
# PHASE 2: DATA CLEANING (5-10 min)
#
echo "================================================================"
echo "PHASE 2: DATA CLEANING (Claude Code)"
echo "================================================================"
echo
echo "This requires Claude Code to process the CSVs."
echo
echo "I'll generate the prompt - you paste it into Claude Code."
echo
read -p "Press ENTER to generate Claude Code prompt..."

cat > "$PROJECT_ROOT/prompts/01-cleaning-prompt.txt" << 'PROMPT_EOF'
I have CSV files from Google Maps scraping in ~/catio-directory/data/raw/

Please clean the data using these criteria:

REMOVE:
1. Missing critical fields (no business name OR no address/city/state)
2. Closed businesses (business_status = CLOSED_PERMANENTLY or CLOSED_TEMPORARILY)
3. Pet stores (PetSmart, Petco, etc.)
4. Big box retailers (Home Depot, Lowe's, etc.)
5. Veterinary clinics
6. Pet grooming (unless name mentions catio/enclosure)
7. General contractors (unless name mentions catio)
8. Exact duplicates (same name + address)
9. Spam (same phone number, different locations)

KEEP:
- Any business with "catio", "cat enclosure", "cat patio" in name
- Pet services IF website exists (we'll verify later)
- Contractors IF website exists
- Fence/deck builders IF catio-related

OUTPUT:
Save to: ~/catio-directory/data/cleaned/catio-builders-cleaned-$(date +%Y%m%d).csv

Also generate a report showing:
- Rows before/after cleaning
- Removal reasons breakdown
- Sample of 20 removed businesses (spot check)
- Geographic distribution of cleaned data

Before starting, show me your game plan.
PROMPT_EOF

echo
echo "✅ Prompt saved to: prompts/01-cleaning-prompt.txt"
echo
echo "NEXT STEPS:"
echo "1. Open Claude Code"
echo "2. Copy/paste the prompt from: cat $PROJECT_ROOT/prompts/01-cleaning-prompt.txt"
echo "3. Let Claude Code process the data"
echo "4. Come back here when it's done"
echo
read -p "Press ENTER when Claude Code cleaning is complete..."

# Verify cleaned data exists
CLEANED_CSV=$(ls -1t "$DATA_DIR/cleaned/"*.csv 2>/dev/null | head -1)
if [ -z "$CLEANED_CSV" ]; then
    echo "❌ ERROR: No cleaned CSV found in data/cleaned/"
    exit 1
fi

echo "✅ Found cleaned data: $CLEANED_CSV"
echo

#
# PHASE 3: INSTALL CRAWL4AI (15-20 min first time, 2 min after)
#
echo "================================================================"
echo "PHASE 3: CRAWL4AI INSTALLATION"
echo "================================================================"
echo

if [ -d "$PROJECT_ROOT/tools/crawl4ai" ]; then
    echo "✅ Crawl4AI already installed, skipping..."
else
    echo "Installing Crawl4AI (this takes ~15 min first time)..."
    echo
    
    mkdir -p "$PROJECT_ROOT/tools"
    cd "$PROJECT_ROOT/tools"
    
    # Check Python version
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    echo "Python version: $PYTHON_VERSION"
    
    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)"; then
        echo "❌ ERROR: Python 3.7+ required"
        exit 1
    fi
    
    # Clone and install
    git clone https://github.com/unclecode/crawl4ai.git
    cd crawl4ai
    pip3 install -r requirements.txt
    pip3 install -e .
    
    # Test installation
    if python3 -c "from crawl4ai import AsyncWebCrawler; print('OK')"; then
        echo "✅ Crawl4AI installed successfully"
    else
        echo "❌ Installation failed"
        exit 1
    fi
fi

cd "$PROJECT_ROOT"
echo

#
# PHASE 4: WEBSITE VERIFICATION (1-3 hours runtime)
#
echo "================================================================"
echo "PHASE 4: WEBSITE VERIFICATION"
echo "================================================================"
echo
echo "This crawls every website to verify they actually build catios."
echo "Runtime: 1-3 hours depending on how many businesses"
echo
read -p "Start verification now? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Generating verification script with Claude Code..."
    
    cat > "$PROJECT_ROOT/prompts/02-verification-prompt.txt" << 'PROMPT_EOF'
Create a Python script: ~/catio-directory/scripts/verify_catio_builders.py

INPUT: ~/catio-directory/data/cleaned/catio-builders-cleaned-LATEST.csv
OUTPUT: ~/catio-directory/data/verified/catio-builders-verified-YYYYMMDD.csv

REQUIREMENTS:
1. Use AsyncWebCrawler from crawl4ai
2. For each business with a website:
   - Crawl homepage + product/service pages
   - Search for catio-related keywords
   - Assign confidence: high/medium/low/none
3. Keywords to search:
   Primary: catio, cat enclosure, cat patio, outdoor cat habitat, cat tunnel
   Secondary: custom pet enclosures + cat, feline outdoor, cat-safe outdoor
4. Confidence scoring:
   HIGH: 2+ primary keywords OR 1 primary + 2 secondary
   MEDIUM: 1 primary OR 3+ secondary
   LOW: 2 secondary OR context clues
   NONE: No match
5. Handle errors (timeout, 404, blocks)
6. Concurrent crawling (10 at a time with semaphore)
7. Save progress every 50 businesses
8. Output columns: all original + verification_status, keywords_found, crawled_at, error_message

Before writing, show me your plan.
PROMPT_EOF

    echo "✅ Prompt saved to: prompts/02-verification-prompt.txt"
    echo
    echo "NEXT: Copy/paste into Claude Code, let it create the script"
    echo
    read -p "Press ENTER when script is created..."
    
    # Run verification script
    if [ -f "$SCRIPTS_DIR/verify_catio_builders.py" ]; then
        echo "Running verification (this takes 1-3 hours)..."
        python3 "$SCRIPTS_DIR/verify_catio_builders.py"
    else
        echo "❌ ERROR: verify_catio_builders.py not found"
        exit 1
    fi
else
    echo "Skipping verification for now."
fi

echo
echo "================================================================"
echo "BUILD STATUS"
echo "================================================================"
echo
echo "✅ Data scraped: $(ls -1 $DATA_DIR/raw/*.csv | wc -l) files"
echo "✅ Data cleaned: $(ls -1 $DATA_DIR/cleaned/*.csv | wc -l) files"
echo "✅ Crawl4AI installed: $([ -d $PROJECT_ROOT/tools/crawl4ai ] && echo 'Yes' || echo 'No')"
echo "✅ Data verified: $(ls -1 $DATA_DIR/verified/*.csv 2>/dev/null | wc -l) files"
echo
echo "NEXT STEPS:"
echo "1. Data enrichment (catio types, sizes, materials)"
echo "2. Build directory website"
echo "3. Deploy to Cloudflare Workers"
echo "4. SEO setup"
echo
echo "Continue with enrichment? (requires Claude API or Claude Code)"
read -p "(y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo "Build paused. Resume anytime by running this script again."
    echo "Your progress is saved in data/verified/"
    exit 0
fi

#
# PHASE 5: DATA ENRICHMENT (1-2 hours)
#
echo "================================================================"
echo "PHASE 5: DATA ENRICHMENT"
echo "================================================================"
echo
echo "Extract: catio types, sizes, materials, features"
echo "Cost: ~\$20-30 if using Claude API, or \$0 with Claude Code"
echo
echo "TODO: Implementation continues..."
echo "(This is where we'd call the enrichment scripts)"
echo

echo
echo "================================================================"
echo "TO BE CONTINUED..."
echo "================================================================"
echo
echo "You've completed the core data pipeline!"
echo "Next: Build the website and deploy"
echo
PROMPT_EOF

chmod +x ~/catio-directory/scripts/BUILD_TONIGHT.sh
