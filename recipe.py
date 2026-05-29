from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


cuisines = [
    "",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek",
    "Korean"
]


dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced"
]


languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Dutch": "nl",
    "Swedish": "sv",
    "Turkish": "tr",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Indonesian": "id",
    "Thai": "th",
    "Filipino": "tl",
    "Vietnamese": "vi"
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        cuisines=cuisines,
        dietary_restrictions=dietary_restrictions,
        languages=languages
    )


@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():
    ingredients = request.form.getlist("ingredient")
    selected_cuisine = request.form.get("cuisine")
    selected_restrictions = request.form.getlist("restrictions")
    selected_language = request.form.get("language")

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."

    prompt = f"""
    Create a recipe using these 3 ingredients:
    {", ".join(ingredients)}.

    Return only valid HTML content.
    Do not include markdown code fences.
    Do not write ```html.
    Do not write ```.
    Start directly with the recipe title.
    Put the ingredients first, then step-by-step instructions.
    """

    if selected_cuisine:
        prompt += f"\nThe cuisine should be {selected_cuisine}."

    if selected_restrictions and len(selected_restrictions) > 0:
        prompt += f"""
        The recipe should follow these dietary restrictions:
        {", ".join(selected_restrictions)}.
        """

    if selected_language:
        prompt += f"""
        Write the entire recipe in this language:
        {selected_language}.
        """

    try:
        response = model.generate_content(prompt)
        recipe = response.text

        recipe = recipe.replace("```html", "")
        recipe = recipe.replace("```", "")
        recipe = recipe.strip()

    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return render_template("recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(debug=True)