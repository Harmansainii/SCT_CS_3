from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def encrypt_decrypt_image(image_path, key, mode):
    img = Image.open(image_path)
    pixels = img.load()

    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]

            if mode == "encrypt":
                pixels[i, j] = (
                    (r + key) % 256,
                    (g + key) % 256,
                    (b + key) % 256
                )
            else:
                pixels[i, j] = (
                    (r - key) % 256,
                    (g - key) % 256,
                    (b - key) % 256
                )

    output_path = os.path.join(OUTPUT_FOLDER, "result.png")
    img.save(output_path)
    return output_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        key = int(request.form["key"])
        mode = request.form["mode"]

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        result_path = encrypt_decrypt_image(file_path, key, mode)

        return send_file(result_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
