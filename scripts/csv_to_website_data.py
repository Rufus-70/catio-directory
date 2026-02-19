#!/usr/bin/env python3
"""
Convert cleaned/verified CSV data into JavaScript for the website

Usage:
    python3 csv_to_website_data.py data/verified/catio-builders-verified-20260218.csv

Output:
    website/data/builders.js
"""

import csv
import json
import sys
from pathlib import Path

def csv_to_json(csv_file):
    """Convert CSV to JSON array"""
    builders = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only include high-confidence verified builders
            if row.get('verification_status') != 'high':
                continue
            
            builder = {
                'name': row.get('name', '').strip(),
                'address': row.get('address', '').strip(),
                'city': row.get('city', '').strip(),
                'state': row.get('state', '').strip(),
                'postalCode': row.get('postalCode', '').strip(),
                'phone': row.get('phone', '').strip(),
                'website': row.get('website', '').strip(),
                'rating': float(row.get('rating', 0)) if row.get('rating') else None,
                'catioTypes': row.get('catio_types', '').split(',') if row.get('catio_types') else [],
                'materials': row.get('materials', '').split(',') if row.get('materials') else [],
                'features': row.get('features', '').split(',') if row.get('features') else [],
            }
            
            # Remove empty fields
            builder = {k: v for k, v in builder.items() if v}
            
            builders.append(builder)
    
    return builders


def group_by_city(builders):
    """Group builders by city for easier browsing"""
    cities = {}
    
    for builder in builders:
        city_key = f"{builder['city']}, {builder['state']}"
        if city_key not in cities:
            cities[city_key] = []
        cities[city_key].append(builder)
    
    # Sort by number of builders (descending)
    sorted_cities = sorted(cities.items(), key=lambda x: len(x[1]), reverse=True)
    
    return dict(sorted_cities)


def generate_js_file(builders, cities, output_file):
    """Generate JavaScript file for website"""
    js_content = f"""// Auto-generated from CSV data
// Generated: {Path(sys.argv[1]).name if len(sys.argv) > 1 else 'unknown'}
// Total builders: {len(builders)}

const BUILDERS_DATA = {json.dumps(builders, indent=2)};

const CITIES_DATA = {json.dumps(cities, indent=2)};

// Helper functions
function getBuildersByCity(city, state) {{
    const key = `${{city}}, ${{state}}`;
    return CITIES_DATA[key] || [];
}}

function searchBuilders(query) {{
    query = query.toLowerCase();
    return BUILDERS_DATA.filter(builder => 
        builder.name.toLowerCase().includes(query) ||
        builder.city.toLowerCase().includes(query) ||
        builder.state.toLowerCase().includes(query)
    );
}}

function filterByType(catioType) {{
    return BUILDERS_DATA.filter(builder =>
        builder.catioTypes && builder.catioTypes.includes(catioType)
    );
}}

// Export for use in website
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ BUILDERS_DATA, CITIES_DATA, getBuildersByCity, searchBuilders, filterByType }};
}}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 csv_to_website_data.py <path_to_verified_csv>")
        print()
        print("Example:")
        print("  python3 csv_to_website_data.py data/verified/catio-builders-verified-20260218.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not Path(csv_file).exists():
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)
    
    print(f"Loading CSV: {csv_file}")
    builders = csv_to_json(csv_file)
    print(f"  → Found {len(builders)} verified builders")
    
    print("Grouping by city...")
    cities = group_by_city(builders)
    print(f"  → {len(cities)} cities with builders")
    
    # Show top cities
    print()
    print("Top 10 cities by builder count:")
    for i, (city, city_builders) in enumerate(list(cities.items())[:10], 1):
        print(f"  {i}. {city}: {len(city_builders)} builders")
    
    # Generate output
    output_file = Path(__file__).parent.parent / 'website' / 'data' / 'builders.js'
    output_file.parent.mkdir(exist_ok=True)
    
    print()
    print(f"Generating JavaScript file: {output_file}")
    generate_js_file(builders, cities, output_file)
    print("  → Done!")
    
    print()
    print("Next steps:")
    print(f"  1. Include in website: <script src='data/builders.js'></script>")
    print(f"  2. Update website/index.html to use BUILDERS_DATA")
    print(f"  3. Deploy website")


if __name__ == '__main__':
    main()
