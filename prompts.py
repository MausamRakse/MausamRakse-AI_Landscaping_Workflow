import json

LANDSCAPE_THEMES = [
    {
        "name": "Modern Minimalist",
        "description": "Clean lines, geometric shapes, and a limited color palette. Features ornamental grasses, succulents, and structural plants like boxwood. Hardscaping includes concrete, metal, and gravel.",
        "keywords": ["modern", "minimalist", "clean", "low-maintenance", "geometric"]
    },
    {
        "name": "English Cottage",
        "description": "Charming, informal, and overflowing with a mix of flowers, herbs, and edibles. Features roses, lavender, and delphiniums. Winding paths and rustic elements like stone and wood are common.",
        "keywords": ["cottage", "charming", "informal", "colorful", "romantic"]
    },
    {
        "name": "Mediterranean",
        "description": "Evokes the feel of a sunny European coast. Features drought-tolerant plants like olive trees, lavender, and rosemary. Terracotta pots, gravel paths, and stucco walls are key elements.",
        "keywords": ["mediterranean", "drought-tolerant", "sunny", "rustic", "herbs"]
    },
    {
        "name": "Japanese Zen",
        "description": "A tranquil and serene space for meditation. Features carefully placed rocks, water elements, moss, and pruned plants like Japanese maples and bonsai. Emphasizes simplicity and natural beauty.",
        "keywords": ["zen", "tranquil", "minimalist", "serene", "asian"]
    },
    {
        "name": "Tropical Paradise",
        "description": "Lush, vibrant, and exotic. Features large-leafed plants like palms, ferns, and banana trees, with bold, bright flowers like hibiscus. Water features and natural stone are common.",
        "keywords": ["tropical", "lush", "vibrant", "exotic", "bold"]
    },
    {
        "name": "Desert Southwest",
        "description": "Inspired by the arid landscapes of Arizona and New Mexico. Features cacti, succulents, and other drought-resistant plants. Hardscaping includes sand, rocks, and rustic wood.",
        "keywords": ["desert", "southwest", "drought-tolerant", "rustic", "succulents"]
    },
    {
        "name": "Coastal",
        "description": "Relaxed and breezy, designed to withstand salt and wind. Features ornamental grasses, hardy perennials, and native coastal plants. Natural materials like driftwood and shells are used.",
        "keywords": ["coastal", "beach", "relaxed", "natural", "wind-resistant"]
    },
    {
        "name": "Woodland",
        "description": "A natural, shady retreat that mimics a forest floor. Features ferns, hostas, and native shade-loving plants and trees. Winding paths and a natural, unkempt look are key.",
        "keywords": ["woodland", "shade", "natural", "forest", "native"]
    },
    {
        "name": "French Country",
        "description": "Formal yet rustic, with lavender fields, vineyards, and formal gardens. Features symmetrical layouts, topiaries, herbs, and fruit trees. Gravel pathways and stone elements are common.",
        "keywords": ["french", "formal", "rustic", "lavender", "herbs"]
    },
    {
        "name": "Urban Edible",
        "description": "Focuses on growing food in a small urban space. Features raised beds, container gardens, and vertical planters for vegetables, herbs, and fruits. Practical and sustainable.",
        "keywords": ["edible", "urban", "vegetable-garden", "sustainable", "small-space"]
    }
]

def get_theme_prompt(customer_input, house_description):
    return f"""
System: You are a landscape design expert. Your task is to recommend the top 3 most suitable landscape themes for a customer based on their preferences, budget, location, and photos of their house.

Analyze the following customer inputs:
- Customer Preferences: {json.dumps(customer_input['preferences'])}
- House Description: {house_description}
- Available Themes: {json.dumps(LANDSCAPE_THEMES)}

Instructions:
1.  Carefully review all the customer inputs and the descriptions of the available landscape themes.
2.  Identify the top 3 themes that best match the customer's needs and the style of their house.
3.  For each recommended theme, provide a brief, compelling rationale (2-3 sentences) explaining why it's a good fit.

Output your response in the following JSON format. Do not include any other text or explanations outside of the JSON structure.

{{
  "recommendations": [
    {{
      "theme_name": "Theme Name 1",
      "rationale": "Your reasoning for why this theme is a great fit."
    }},
    {{
      "theme_name": "Theme Name 2",
      "rationale": "Your reasoning for why this theme is a great fit."
    }},
    {{
      "theme_name": "Theme Name 3",
      "rationale": "Your reasoning for why this theme is a great fit."
    }}
  ]
}}
"""

def get_overhead_prompt(customer_input, theme):
    return f"""
System: You are an expert landscape designer AI. Your task is to create a detailed, conceptual overhead landscape plan based on a chosen design theme and customer preferences. You will not be given a satellite image.

Inputs:
- Address: {customer_input['address']}
- Chosen Theme: {json.dumps(theme)}
- Customer Preferences: {json.dumps(customer_input['preferences'])}

Instructions:
1.  Based on the '{theme['name']}' theme and the customer's preferences, design a conceptual landscape layout for a typical property at the given address.
2.  Assume a standard rectangular front yard and a side yard area.
3.  The design should be practical, aesthetically pleasing, and respect the customer's budget and maintenance level.
4.  Generate a detailed plan as a JSON object that specifies the placement of plants, hardscaping elements (patios, paths, etc.), and other features.
5.  Generate a textual description for a new rendered image of this conceptual overhead plan. This description should be detailed enough for an image generation model to create a visual representation.

Output your response in the following JSON format ONLY:

{{
  "json_plan": {{
    "zones": [
      {{
        "zone_id": "front_yard",
        "description": "The main area facing the street.",
        "features": [
          {{
            "type": "pathway",
            "material": "flagstone",
            "description": "A gently curving pathway from the driveway to the front door."
          }},
          {{
            "type": "planting_bed",
            "plants": ["Lavender", "Rosemary", "Boxwood"],
            "description": "A planting bed along the front of the house."
          }}
        ]
      }},
      {{
        "zone_id": "side_yard",
        "description": "The area on the side of the house.",
        "features": [
          {{
            "type": "utility_area",
            "description": "A gravel area for trash bin storage, screened by a wooden lattice."
          }}
        ]
      }}
    ]
  }},
  "rendered_image_prompt": "A detailed, realistic, top-down satellite-style concept view of a suburban house at {customer_input['address']}. The landscape is designed in the {theme['name']} style. A new flagstone pathway curves from the driveway to the front door. Lush planting beds with lavender and boxwood are visible in the front yard. The side yard has a discreet gravel utility area hidden by a screen. The image should be a conceptual rendering, not based on a real satellite photo."
}}
"""

VISION_DESCRIPTION_PROMPT = """
System: You are an expert architectural and landscape analyst. Your task is to analyze an image of a house and its surrounding area to provide a concise, descriptive summary for a landscape designer.

Instructions:
1.  Examine the provided image of the house.
2.  Note the architectural style (e.g., Modern, Colonial, Ranch, etc.).
3.  Describe the exterior materials and colors (e.g., red brick, white siding, dark roof).
4.  Identify any existing landscaping, pathways, or driveways.
5.  Describe the overall impression of the property.
6.  Keep the description to 4-5 sentences.

Example: "The image shows a two-story Colonial-style house with a red brick facade and white trim. A concrete driveway leads to a two-car garage on the left. The existing landscaping is minimal, consisting of a small lawn and a few overgrown shrubs near the foundation. The overall impression is traditional and could be enhanced with more structured and colorful landscaping."

Begin your analysis of the attached image now.
"""

def get_before_after_prompt(house_description, theme):
    return f"""
System: You are an AI image generation expert specializing in photorealistic architectural rendering.

Instructions:
1.  You will be given a description of a house and a desired landscape theme.
2.  Generate a single, photorealistic, high-resolution image of the house with the new landscaping applied.
3.  The final image should look like a realistic "After" photo from a professional landscaping project.
4.  Pay close attention to lighting, shadows, and textures to ensure realism.

Inputs:
- House Description: {house_description}
- Landscape Theme: {theme['name']}
- Theme Description: {theme['description']}

Generate the image now.
"""

def get_materials_prompt(customer_input, theme):
    return f"""
System: You are a landscape supply chain expert. Your task is to generate a detailed list of materials required for a landscaping project based on a chosen theme.

Inputs:
- Chosen Theme: {json.dumps(theme)}
- Customer Preferences: {json.dumps(customer_input['preferences'])}
- Location: {customer_input['address']}

Instructions:
1.  Based on the '{theme['name']}' theme, create a comprehensive list of suggested plants and hardscaping materials.
2.  For each plant, provide its name, suggested quantity, ideal placement, approximate cost range per unit, sunlight needs, and any important soil notes.
3.  For hardscaping materials, list the material, suggested quantity (e.g., in sq. ft. or cubic yards), and an approximate cost range.
4.  Ensure the suggestions are appropriate for the general climate of the provided address and align with the customer's budget and maintenance preferences.

Output your response in the following JSON format ONLY:

{{
  "materials": [
    {{
      "item_type": "plant",
      "name": "Lavender",
      "quantity": 10,
      "placement": "Front yard planting beds, along pathways.",
      "cost_range_per_unit": "$10-$20",
      "sunlight_needs": "Full Sun",
      "soil_notes": "Well-drained, alkaline soil."
    }},
    {{
      "item_type": "plant",
      "name": "Boxwood",
      "quantity": 8,
      "placement": "As a low hedge to define garden beds.",
      "cost_range_per_unit": "$25-$40",
      "sunlight_needs": "Full Sun to Part Shade",
      "soil_notes": "Tolerant of most soil types, prefers well-drained."
    }},
    {{
      "item_type": "hardscape",
      "name": "Flagstone",
      "quantity": "150 sq. ft.",
      "cost_range_per_unit": "$5-$8 per sq. ft.",
      "placement": "Front pathway and small patio.",
      "notes": "Choose a non-slip variety."
    }},
    {{
      "item_type": "hardscape",
      "name": "Mulch",
      "quantity": "5 cubic yards",
      "cost_range_per_unit": "$30-$50 per cubic yard",
      "placement": "All planting beds.",
      "notes": "Use cedar or cypress for natural pest resistance."
    }}
  ]
}}
"""
