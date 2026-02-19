// REAL verified catio builders - scraped from Google Maps
// Generated: 2026-02-18
// Total builders: 6

const BUILDERS_DATA = [
  {
    "name": "Portland Catios",
    "address": "Happy Valley",
    "city": "Portland",
    "state": "OR",
    "postalCode": "97086",
    "website": "https://portlandcatios.com",
    "rating": 5.0,
    "catioTypes": ["window_box", "patio", "standalone", "tunnel"],
    "materials": ["powder_coated_aluminum", "welded"],
    "features": ["custom_design", "weatherproof", "multi_level", "professional_install", "premium"],
    "verified": true
  },
  {
    "name": "The Catio Company",
    "city": "Austin",
    "state": "TX",
    "website": "http://thecatiocompany.com/",
    "rating": 4.7,
    "catioTypes": ["window_box", "patio", "standalone"],
    "materials": ["cedar", "aluminum"],
    "features": ["diy_kits", "custom_design"],
    "verified": true
  },
  {
    "name": "Catio Craftsman LLC",
    "address": "NW Sluman Rd",
    "city": "Vancouver",
    "state": "WA",
    "postalCode": "98665",
    "phone": "(206) 636-1209",
    "website": "http://www.catiocraftsman.com/",
    "rating": 4.9,
    "catioTypes": ["window_box", "patio", "standalone", "tunnel"],
    "materials": ["cedar", "aluminum", "pet_screen"],
    "features": ["professional_install", "custom_design", "pnw_specialist"],
    "verified": true
  },
  {
    "name": "Custom Catios",
    "city": "Los Angeles",
    "state": "CA",
    "phone": "(323) 905-4695",
    "website": "https://customcatios.com/",
    "catioTypes": ["patio", "standalone", "custom"],
    "materials": ["wood", "metal"],
    "features": ["custom_design", "nationwide"],
    "verified": true
  },
  {
    "name": "Cool Cat Fence",
    "city": "Seattle",
    "state": "WA",
    "website": "https://coolcatfence.com/",
    "catioTypes": ["patio", "standalone", "fence"],
    "materials": ["wood", "mesh"],
    "features": ["cat_fencing", "outdoor_enclosures"],
    "verified": true
  },
  {
    "name": "Cool Catios",
    "city": "Online",
    "state": "",
    "website": "http://coolcatios.com/",
    "catioTypes": ["window_box", "patio", "standalone"],
    "materials": ["various"],
    "features": ["custom_design"],
    "verified": true
  }
];

const CITIES_DATA = {
  "Portland, OR": [BUILDERS_DATA[0]],
  "Austin, TX": [BUILDERS_DATA[1]],
  "Vancouver, WA": [BUILDERS_DATA[2]],
  "Los Angeles, CA": [BUILDERS_DATA[3]],
  "Seattle, WA": [BUILDERS_DATA[4]]
};

function getBuildersByCity(city, state) {
    const key = city + ", " + state;
    return CITIES_DATA[key] || [];
}

function searchBuilders(query) {
    query = query.toLowerCase();
    return BUILDERS_DATA.filter(function(builder) {
        return builder.name.toLowerCase().includes(query) ||
            (builder.city && builder.city.toLowerCase().includes(query)) ||
            (builder.state && builder.state.toLowerCase().includes(query));
    });
}

function filterByType(catioType) {
    return BUILDERS_DATA.filter(function(builder) {
        return builder.catioTypes && builder.catioTypes.includes(catioType);
    });
}
