from google import genai
from google.genai import types
import mimetypes
import os
import pathlib
from flask import Flask, request, render_template

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyAgpnHJk6J4muiywIy0TTl5iH2xCYtei4U")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    anything = request.form['anything']
    selected_era = request.form['era']
    selected_pattern = request.form['pattern']
    selected_color = request.form['color']
    selected_species = request.form['species']

    prompt = f"Generate an image for a {selected_species} with a pattern of {selected_pattern} on its body, and the color {selected_color} for its skin theme. The design of the animal should represent its time period the {selected_era} era. If it is the future, then incorporate tech, cyber or punk inspired features to make it seem half-robot or mechanical. If its from the present depict it as a modern realistic version. If its from the past design it as an ancient form or, an ancestral form of the in the dinosaur age or ice age with intimidating features of the animal (for example bigger fangs or claws, smaller less-cute eyes, more hunter-like ONLY IF IT IS PREHISTORIC). The style of the art  should incoroporate elements of geometric abltractions and a slightly stylized vector like aesthetic. the animal should be full body and upright or sitting, DO NOT just give me a portrait view. also add {anything}. make sure there is a black background and ensure it has all limbs. MAKE SURE TO FOLLOW The art STYLE AND BLACK BACKGROUND."

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            data = part.inline_data.data
            pathlib.Path("static/img.png").write_bytes(data)

    return render_template("result.html", image_url="/static/img.png",
    selected_color=selected_color,
    selected_species=selected_species,
    selected_pattern=selected_pattern,
    selected_era=selected_era)



if __name__ == '__main__':
    app.run(debug=True)