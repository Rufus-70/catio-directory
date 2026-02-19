# Step 3: Crawl4AI Installation & Setup

## What is Crawl4AI?

**Crawl4AI**: Open-source LLM-friendly web crawler and scraper
- **Cost**: FREE (runs locally on your machine)
- **Purpose**: Visit every business website and verify they actually build catios
- **Benefit**: Saves 1,000+ hours of manual website checking

**GitHub**: https://github.com/unclecode/crawl4ai

---

## Installation (WSL2/Linux)

### Let Claude Code Do It For You

**Easiest Method**: Copy this prompt into Claude Code:

```
Please help me install Crawl4AI on my WSL2 Ubuntu system.

GitHub repo: https://github.com/unclecode/crawl4ai

Follow the installation instructions from the README, and:
1. Check if I have the required dependencies (Python 3.7+, pip)
2. Install any missing dependencies
3. Clone the repo to ~/catio-directory/tools/crawl4ai/
4. Install the package
5. Verify the installation works with a simple test

If you encounter any errors, troubleshoot and fix them.
```

### Manual Installation (If Needed)

```bash
# Check Python version (need 3.7+)
python3 --version

# Install pip if missing
sudo apt update
sudo apt install python3-pip -y

# Clone Crawl4AI
cd ~/catio-directory/tools/
git clone https://github.com/unclecode/crawl4ai.git
cd crawl4ai

# Install dependencies
pip3 install -r requirements.txt

# Install the package
pip3 install -e .

# Test installation
python3 -c "from crawl4ai import AsyncWebCrawler; print('Success!')"
```

---

## Important Modules to Enable

### AsyncWebCrawler (Speed Optimization)

From Frey's guide:
> "async_webcrawler allows you to crawl multiple websites concurrently. That saves a ton of time."

**Enable it in your scripts**:
```python
from crawl4ai import AsyncWebCrawler
```

This lets you crawl 10-20 websites simultaneously instead of one at a time.

---

## Testing Crawl4AI

### Test with a known catio builder website:

```python
# test_crawl.py
from crawl4ai import AsyncWebCrawler
import asyncio

async def test_crawl():
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Test with Portland Catios website (yours!)
        result = await crawler.arun(
            url="https://portlandcatios.com",  # Replace with actual URL
            word_count_threshold=50,
            bypass_cache=True
        )
        
        print(f"URL: {result.url}")
        print(f"Success: {result.success}")
        print(f"Extracted text length: {len(result.extracted_content)}")
        print("\n--- First 500 characters ---")
        print(result.extracted_content[:500])

asyncio.run(test_crawl())
```

**Run it**:
```bash
python3 test_crawl.py
```

**Expected output**:
- Success: True
- Extracted text showing your catio services, materials, etc.

---

## Common Installation Issues

### Issue 1: "ModuleNotFoundError: No module named 'crawl4ai'"

**Solution**: Install in editable mode
```bash
cd ~/catio-directory/tools/crawl4ai
pip3 install -e .
```

### Issue 2: "playwright install required"

Some versions need Playwright for browser automation:
```bash
pip3 install playwright
playwright install
```

### Issue 3: "Permission denied"

Add yourself to the right group:
```bash
sudo usermod -a -G dialout $USER
# Logout and log back in
```

### Issue 4: Memory errors with large batches

Reduce concurrent crawls from 20 to 5-10:
```python
semaphore = asyncio.Semaphore(5)  # Max 5 concurrent
```

---

## File Structure After Installation

```
~/catio-directory/
├── README.md
├── data/
│   ├── raw/              # OutScraper CSVs
│   ├── cleaned/          # After Claude Code cleaning
│   └── verified/         # After Crawl4AI verification (next step)
├── tools/
│   └── crawl4ai/         # Crawl4AI installation
└── scripts/
    └── verify_catio_builders.py  # We'll create this in Step 4
```

---

## Next Step

Once Crawl4AI is installed and tested, move to **Step 4: Website Verification with Crawl4AI + Claude Code**

---

## Pro Tips

1. **Run overnight**: Crawling 500-3,000 websites takes 2-6 hours depending on your connection
2. **Save progress**: The script should save partial results every 50-100 sites
3. **Handle errors gracefully**: Some websites will timeout or block you - that's normal
4. **Respect rate limits**: Don't crawl the same domain repeatedly (you'll get IP banned)

---

## Troubleshooting Command

If you get stuck, run this diagnostic:

```bash
# Check Python version
python3 --version

# Check if Crawl4AI is importable
python3 -c "from crawl4ai import AsyncWebCrawler; print('Crawl4AI OK')"

# Check pip packages
pip3 list | grep -i crawl

# Check installation path
which python3
```

Paste results into Claude Code and ask it to debug.
