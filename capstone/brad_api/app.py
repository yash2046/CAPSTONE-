from flask import Flask, render_template, request, jsonify
import google.generativeai as palm

app = Flask(__name__, template_folder="./templates/")

Api_key = "AIzaSyDe-jrC-N0we9M6oTMiCu_rx_ipfPUa11s"
palm.configure(api_key=Api_key)

models = [
    m for m in palm.list_models() if "generateText" in m.supported_generation_methods
]

model = models[0].name

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0.3,
            max_output_tokens=800,
        )

        response = completion.result

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
