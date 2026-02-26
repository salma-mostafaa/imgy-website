from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64

app = Flask(__name__)

def encode(img):
    _, buf = cv2.imencode(".png", img)
    return "data:image/png;base64," + base64.b64encode(buf).decode()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():

    file1 = request.files["image"]
    nparr = np.frombuffer(file1.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img2 = None
    if "image2" in request.files:
        file2 = request.files["image2"]
        nparr2 = np.frombuffer(file2.read(), np.uint8)
        img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)
        if img2 is not None:
            img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))

    op = request.form["operation"]

    if op == "addition" and img2 is not None:
        result = cv2.add(img, img2)

    elif op == "subtraction" and img2 is not None:
        g1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        g2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        result = cv2.subtract(g1, g2)

    elif op == "hist_match" and img2 is not None:
        from skimage import exposure
        src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ref = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        result = exposure.match_histograms(src,ref)

    elif op == "const_sub":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.subtract(gray, 128)

    elif op == "const_sub_np":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = np.clip(gray - 128, 0, 255).astype(np.uint8)

    elif op == "negative":
        result = 255 - img

    elif op == "bit_plane":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bit = int(request.form.get("bit", 7))
        result = ((gray >> bit) & 1) * 255

    elif op == "intensity_slice":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = np.zeros_like(gray)
        result[(gray > 51) & (gray < 140)] = 255

    elif op == "canny":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        low = int(request.form.get("low", 100))
        high = int(request.form.get("high", 200))
        result = cv2.Canny(gray, low, high)

    elif op == "sobel":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
        result = cv2.convertScaleAbs(sx + sy)

    elif op == "laplacian":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_64F))

    elif op == "mean":
        result = cv2.blur(img, (5,5))

    elif op == "gaussian":
        result = cv2.GaussianBlur(img, (5,5), 0)

    elif op == "median":
        result = cv2.medianBlur(img, 5)

    elif op == "unsharp":
        blur = cv2.GaussianBlur(img, (25,25), 0)
        result = cv2.addWeighted(img, 1.5, blur, -0.5, 0)

    elif op == "shear":
        shx = float(request.form.get("shx", 0))
        shy = float(request.form.get("shy", 0))
        h, w = img.shape[:2]
        M = np.array([[1, shx, 0],[shy, 1, 0]], np.float32)
        result = cv2.warpAffine(img, M, (w, h))

    elif op == "translate":
        tx = int(request.form.get("tx", 100))
        ty = int(request.form.get("ty", 70))
        h, w = img.shape[:2]
        M = np.array([[1,0,tx],[0,1,ty]], np.float32)
        result = cv2.warpAffine(img, M, (w,h))

    elif op == "rotate":
        angle = float(request.form.get("angle", 30))
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
        result = cv2.warpAffine(img, M, (w,h))

    elif op == "log" or op == "inv_log":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        c = float(request.form.get("c", 5))
        log_img = c * np.log(gray + 1)
        if op == "inv_log":
            log_img = c * (np.exp(log_img / c) - 1)
        result = np.uint8(log_img)

    elif op == "mask":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(gray)
        mask = cv2.rectangle(mask, (200,300), (600,1000), 1, -1)
        result = cv2.multiply(gray, mask)

    else:
        result = img

    return jsonify(image=encode(result))

if __name__ == "__main__":
    app.run(debug=True)
