import base64
import os
from prompts import (
    LANDSCAPE_THEMES,
    get_theme_prompt,
    get_overhead_prompt,
    VISION_DESCRIPTION_PROMPT,
    get_before_after_prompt,
    get_materials_prompt
)
import gemini_helper as gemini
from pdf_generator import generate_pdf_report

class LandscapeAI:
    def __init__(self, api_keys):
        """
        Initializes the LandscapeAI agent.
        
        Args:
            api_keys (dict): A dictionary containing 'gemini' API key.
        """
        if not api_keys.get('gemini'):
            raise ValueError("API key for Gemini is required.")
        
        self.api_keys = api_keys
        gemini.init_gemini(api_keys['gemini'])

    def _score_theme(self, theme, preferences):
        """
        Scores a theme based on customer preferences.
        """
        score = 0
        if preferences.get('maintenance_level') == 'low' and 'low-maintenance' in theme['keywords']:
            score += 2
        if preferences.get('sunlight') == 'full_sun' and 'sunny' in theme['keywords']:
            score += 1
        if preferences.get('budget') == 'high' and ('formal' in theme['keywords'] or 'lush' in theme['keywords']):
            score += 1
        
        # Simple color matching
        preferred_colors = set(preferences.get('colors', []))
        theme_colors = set(theme.get('keywords', []))
        if preferred_colors.intersection(theme_colors):
            score += 1
            
        return score

    async def select_theme(self, customer_input):
        """
        Analyzes customer input and selects the best landscape theme.
        """
        print("Step 2: Selecting Theme...")
        # Get a description of the house from the front image
        front_image_b64 = customer_input['images']['front']['base64']
        front_image_mime = customer_input['images']['front']['mime_type']
        house_description = gemini.analyze_image(front_image_b64, front_image_mime, VISION_DESCRIPTION_PROMPT)
        
        print("-> Analyzing house style...")
        # Get theme recommendations from Gemini
        prompt = get_theme_prompt(customer_input, house_description)
        recommendations = gemini.generate_text(prompt)['recommendations']
        
        print(f"-> Gemini Recommendations: {[rec['theme_name'] for rec in recommendations]}")
        
        # Score the recommended themes
        best_theme = None
        max_score = -1

        for rec in recommendations:
            theme_name = rec['theme_name']
            theme_details = next((t for t in LANDSCAPE_THEMES if t['name'] == theme_name), None)
            if theme_details:
                score = self._score_theme(theme_details, customer_input['preferences'])
                print(f"   - Scoring '{theme_name}': {score}")
                if score > max_score:
                    max_score = score
                    best_theme = theme_details
        
        if not best_theme:
            best_theme = next((t for t in LANDSCAPE_THEMES if t['name'] == recommendations[0]['theme_name']), LANDSCAPE_THEMES[0])

        print(f"-> Final Theme Selected: {best_theme['name']}")
        return best_theme

    async def generate_overhead(self, customer_input, theme):
        """
        Generates the conceptual overhead layout plan and rendered image.
        """
        print("Step 3.1: Generating Overhead Layout...")
        
        prompt = get_overhead_prompt(customer_input, theme)
        
        print("-> Generating conceptual JSON plan and render prompt...")
        # This now generates a conceptual plan without a map image
        overhead_data = gemini.generate_text(prompt)

        print("-> Generating rendered overhead image...")
        rendered_image_b64 = gemini.generate_image(overhead_data['rendered_image_prompt'])
        
        return {
            "json_plan": overhead_data['json_plan'],
            "rendered_image_base64": rendered_image_b64
        }

    async def generate_before_after(self, customer_input, theme):
        """
        Generates the 'after' image render.
        """
        print("Step 3.2: Generating Before & After Render...")
        front_image_b64 = customer_input['images']['front']['base64']
        front_image_mime = customer_input['images']['front']['mime_type']

        print("-> Analyzing front house image...")
        house_description = gemini.analyze_image(front_image_b64, front_image_mime, VISION_DESCRIPTION_PROMPT)
        
        prompt = get_before_after_prompt(house_description, theme)
        
        print("-> Generating 'After' render...")
        after_image_b64 = gemini.generate_image(prompt)
        
        return {
            "before_image_base64": front_image_b64,
            "after_image_base64": after_image_b64
        }

    async def generate_materials(self, customer_input, theme):
        """
        Generates the material list.
        """
        print("Step 3.3: Generating Material List...")
        prompt = get_materials_prompt(customer_input, theme)
        materials_data = gemini.generate_text(prompt)
        return materials_data['materials']

    def package_output(self, theme, overhead, before_after, materials):
        """
        Packages all the generated artifacts into a single JSON object.
        """
        print("Step 4: Packaging Output...")
        summary = f"Landscape AI design package for {self.customer_name}. The selected theme is '{theme['name']}', which aligns with your preferences for a {self.customer_input['preferences']['maintenance_level']} maintenance and {self.customer_input['preferences']['budget']} budget."

        output = {
            "theme_selected": theme,
            "overhead_plan": overhead,
            "before_after": before_after,
            "materials": materials,
            "summary_report": summary
        }
        print("Workflow Complete!")
        return output

    async def run_workflow(self, customer_input):
        """
        Runs the full landscaping AI workflow.
        """
        print(f"Starting Landscape AI workflow for {customer_input['customer_name']}...")
        self.customer_name = customer_input['customer_name']
        self.customer_input = customer_input

        # STEP 2
        theme = await self.select_theme(customer_input)
        
        # STEP 3
        overhead = await self.generate_overhead(customer_input, theme)
        before_after = await self.generate_before_after(customer_input, theme)
        materials = await self.generate_materials(customer_input, theme)
        
        # STEP 4
        final_package = self.package_output(theme, overhead, before_after, materials)
        
        return final_package

async def main():
    """
    Main function to run a test case.
    """
    from dotenv import load_dotenv
    import json
    load_dotenv()

    api_keys = {
        "gemini": os.getenv("GEMINI_API_KEY"),
    }

    # Helper to encode local images to base64
    def image_to_base64(filepath):
        with open(filepath, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    # Create dummy images for testing
    if not os.path.exists("dummy_front.jpg"):
        from PIL import Image
        Image.new('RGB', (600, 400), color = 'red').save('dummy_front.jpg')
    if not os.path.exists("dummy_side.jpg"):
        from PIL import Image
        Image.new('RGB', (600, 400), color = 'blue').save('dummy_side.jpg')


    # --- Test Customer Input ---
    customer_input = {
        "customer_name": "John Doe",
        "address": "1600 Amphitheatre Parkway, Mountain View, CA",
        "images": {
            "front": {
                "base64": image_to_base64("dummy_front.jpg"),
                "mime_type": "image/jpeg"
            },
            "side": {
                "base64": image_to_base64("dummy_side.jpg"),
                "mime_type": "image/jpeg"
            }
        },
        "preferences": {
            "budget": "moderate",
            "maintenance_level": "low",
            "sunlight": "full_sun",
            "preferred_colors": ["blue", "purple", "white"]
        }
    }
    # --------------------------

    agent = LandscapeAI(api_keys)
    result = await agent.run_workflow(customer_input)

    # Save result to a file
    with open("landscape_design_output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("\n✅ Output saved to landscape_design_output.json")
    
    # Generate PDF report
    generate_pdf_report(result)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
