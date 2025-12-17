from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64

app = Flask(__name__)
current_img = None  # stores current image for overlapping

def encode(img):
    _, buf = cv2.imencode(".png", img)
    return "data:image/png;base64," + base64.b64encode(buf).decode()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reset")
def reset():
    global current_img
    current_img = None
    return jsonify(ok=True)

@app.route("/process", methods=["POST"])
def process():
    global current_img

    # Load main image
    if current_img is None:
        file1 = request.files["image"]
        nparr = np.frombuffer(file1.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        current_img = img.copy()
    else:
        img = current_img.copy()

    # Optional second image
    img2 = None
    if "image2" in request.files:
        file2 = request.files["image2"]
        nparr2 = np.frombuffer(file2.read(), np.uint8)
        img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)
        if img2 is not None:
            img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))

    op = request.form["operation"]

    # ================= Two-Image Operations =================
    if op == "addition" and img2 is not None:
        result = cv2.add(img, img2)
    elif op == "subtraction" and img2 is not None:
        gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        result = cv2.subtract(gray1, gray2)
    elif op == "division" and img2 is not None:
        result = img / (img2 + 1)
    elif op == "hist_match" and img2 is not None:
        src_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ref_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        result = cv2.normalize(src_gray, None, 0, 255, cv2.NORM_MINMAX)

    # ================= Arithmetic / Intensity =================
    elif op == "const_sub":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.subtract(gray, 128)
    elif op == "const_sub_np":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = gray - 128
    elif op == "negative":
        result = 255 - img
    elif op == "normalize":
        result = cv2.normalize(img.astype("float"), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # ================= Bit & Slicing =================
    elif op == "bit_plane":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bit = int(request.form.get("bit", 7))
        result = np.bitwise_and(gray, 1 << bit)
    elif op == "intensity_slice":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = np.zeros(gray.shape, dtype=np.uint8)
        result[(gray > 51) & (gray < 140)] = 255

    # ================= Edge Detection =================
    elif op == "canny":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        low = int(request.form.get("low", 100))
        high = int(request.form.get("high", 200))
        result = cv2.Canny(gray, low, high)
    elif op == "sobel":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        sx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=5)
        sy = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=5)
        result = cv2.convertScaleAbs(sx + sy)
    elif op == "laplacian":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (3,3))
        lap = cv2.Laplacian(blur, cv2.CV_64F)
        result = cv2.convertScaleAbs(lap)

    # ================= Filtering =================
    elif op == "mean":
        result = cv2.blur(img, (5,5))
    elif op == "gaussian":
        result = cv2.GaussianBlur(img, (5,5), 0)
    elif op == "median":
        result = cv2.medianBlur(img, 5)
    elif op == "unsharp":
        blur = cv2.GaussianBlur(img, (25,25), 0)
        mask = cv2.subtract(img, blur)
        result = cv2.add(img, mask)

    # ================= Geometric / Transform =================
    elif op == "shear":
        h, w = img.shape[:2]
        shx = float(request.form.get("shx", 0)) 
        shy = float(request.form.get("shy", 0))  
        M = np.array([[1, shx, 0],
                  [shy, 1, 0]], dtype=np.float32)
        result = cv2.warpAffine(img, M, (w,h))
    elif op == "translate":
        tx = int(request.form.get("tx", 100))
        ty = int(request.form.get("ty", 70))
        h, w = img.shape[:2]
        M = np.array([[1,0,tx],[0,1,ty]], dtype=np.float32)
        result = cv2.warpAffine(img, M, (w,h))
    elif op == "rotate":
        angle = float(request.form.get("angle", 30))
        h, w = img.shape[:2]
        center = (w//2, h//2)
        M = cv2.getRotationMatrix2D(center, angle, 1)
        result = cv2.warpAffine(img, M, (w,h))

    # ================= Log / Inverse Log =================
    elif op == "log" or op == "inv_log":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        c = float(request.form.get("c", 5))
        log_img = c * np.log(gray + 1)
        if op == "inv_log":
            log_img = c * (np.exp(log_img / c) - 1)
        result = np.uint8(log_img)

    # ================= Masking =================
    elif op == "mask":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = np.zeros(gray.shape, dtype=np.uint8)
        mask = cv2.rectangle(mask, (200,300),(600,1000), 1,-1)
        result = cv2.multiply(gray, mask)

    else:
        result = img

    current_img = result.copy()
    return jsonify(image=encode(result))

if __name__ == "__main__":
    app.run(debug=True)
