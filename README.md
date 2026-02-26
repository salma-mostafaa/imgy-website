# IMGY 🖼️✨

An Online Image Processing web-based application for performing a wide range **image processing operations** online, including arithmetic operations, edge detection, filtering, geometric transformations, bit slicing, and more. Built using **HTML, CSS, JavaScript, and Python Flask** with **OpenCV** for image processing.

---

## Features

- **Two-Image Operations**
  - Addition
  - Subtraction
  - Division
  - Histogram Matching
- **Arithmetic / Intensity Operations**
  - Constant Subtraction
  - Negative Image
  - Normalization
- **Bit & Intensity Slicing**
  - Bit Plane Slicing
  - Intensity Level Slicing
- **Edge Detection**
  - Canny Edge Detector
  - Sobel Operator
  - Laplacian Filter
- **Filtering**
  - Mean, Gaussian, Median Filters
  - Unsharp Masking
- **Geometric Transformations**
  - Shearing
  - Translation
  - Rotation
- **Logarithmic Transforms**
  - Log Transform
  - Inverse Log Transform
- **Masking**
  - Apply a custom mask to images

Additional features include **live preview**, **parameter adjustments**, **reset**, and **download processed images**.

---

## Demo

![Demo Screenshot](/css/birds.jpg)  
*Sample image preview before processing.*

---

## Technologies Used

- **Frontend**
  - HTML5
  - CSS3 (responsive design for mobile and desktop)
  - JavaScript (dynamic form handling and image preview)
- **Backend**
  - Python 3
  - Flask (web framework)
  - OpenCV (image processing)
  - NumPy (numerical operations)
- **Image Handling**
  - Base64 encoding for displaying processed images in the browser

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/online-image-processing.git
   cd online-image-processing
   ```

2. **Install dependencies**  
   ```bash
   pip install flask opencv-python numpy
   cd online-image-processing
   ```

3. **Run the application**  
   ```bash
   python app.py
   ```

---
**Usage**

1. Open the app in a browser.
2. Upload your main image (and optional second image for two-image operations).
3. Select the operation you want to perform.
4. Adjust the parameters if required (e.g., shear, rotation, bit plane, etc.).
5. Click Process to see the result.
6. Use Reset to revert to the original image.
7. Click Download to save the processed image.

---
**File Structure**
```
├── app.py              # Flask backend
├──  index.html         # Frontend HTML
|── css/
│    │ └── styles.css   # Styling
|    └── birds.jpg      # Sample image
|─ js/
│     └── script.js     # Frontend logic
│         
└── README.md           # Project documentation
```
---
**Notes**
1. Images are processed on the server using OpenCV and returned as Base64 encoded PNG.
2. The app supports both color and grayscale operations.
3. Ensure uploaded images are in standard formats (PNG, JPG, JPEG).
4. Some operations require two images (e.g., addition, subtraction, histogram matching).

---
