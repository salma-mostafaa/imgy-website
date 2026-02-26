const uploadForm = document.getElementById("uploadForm");
const imageInput = document.getElementById("image");
const operationSelect = document.getElementById("operation");

const logBox = document.getElementById("logBox");
const translateBox = document.getElementById("translateBox");
const rotateBox = document.getElementById("rotateBox");
const bitBox = document.getElementById("bitBox");
const cannyBox = document.getElementById("cannyBox");
const shearBox = document.getElementById("shearBox");


const outputImage = document.getElementById("outputImage");
const resetBtn = document.getElementById("resetBtn");
const downloadBtn = document.getElementById("downloadBtn");

let originalFile = null; // store original File for FormData
let originalImageSrc = null;

// ------------------ Show/Hide parameters ------------------
function hideAllParams() {
    logBox.style.display = "none";
    translateBox.style.display = "none";
    rotateBox.style.display = "none";
    bitBox.style.display = "none";
    cannyBox.style.display = "none";
}

operationSelect.addEventListener("change", () => {
    hideAllParams();
    const op = operationSelect.value;
    if (op === "log" || op === "inv_log") logBox.style.display = "block";
    else if (op === "translate") translateBox.style.display = "block";
    else if (op === "rotate") rotateBox.style.display = "block";
    else if (op === "bit_plane") bitBox.style.display = "block";
    else if (op === "canny") cannyBox.style.display = "block";
    else if (op == "shear") shearBox.style.display ="block";
});

// ------------------ Show original immediately ------------------
imageInput.addEventListener("change", (e) => {
    originalFile = e.target.files[0];
    if (!originalFile) return;
    const reader = new FileReader();
    reader.onload = () => {
        outputImage.src = reader.result;
        originalImageSrc = reader.result;
    };
    reader.readAsDataURL(originalFile);
});

// ------------------ Process Image ------------------
uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!originalFile) return alert("Please upload an image first!");

    const formData = new FormData();
    formData.append("image", originalFile);
    if (document.getElementById("image2").files[0]) {
        formData.append("image2", document.getElementById("image2").files[0]);
    }
    formData.append("operation", operationSelect.value);

    // Add parameters if relevant
    if (operationSelect.value === "log" || operationSelect.value === "inv_log") {
        formData.append("c", document.getElementById("cVal").value);
    } else if (operationSelect.value === "translate") {
        formData.append("tx", document.getElementById("tx").value);
        formData.append("ty", document.getElementById("ty").value);
    } else if (operationSelect.value === "rotate") {
        formData.append("angle", document.getElementById("angle").value);
    } else if (operationSelect.value === "bit_plane") {
        formData.append("bit", document.getElementById("bit").value);
    } else if (operationSelect.value === "canny") {
        formData.append("low", document.getElementById("low").value);
        formData.append("high", document.getElementById("high").value);
    }else if (operationSelect.value === "shear") {
        formData.append("shx", document.getElementById("shx").value);
        formData.append("shy", document.getElementById("shy").value);
    }

    const response = await fetch("https://salma5mostafa.pythonanywhere.com/process", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    outputImage.src = data.image;
});

// ------------------ Reset ------------------
resetBtn.addEventListener("click", () => {
        fetch("https://salma5mostafa.pythonanywhere.com/reset")
        .then(() => {
            if (originalImageSrc) outputImage.src = originalImageSrc;
        });
});

// ------------------ Download ------------------
downloadBtn.addEventListener("click", () => {
    if (!outputImage.src) return alert("No processed image to download");
    const a = document.createElement("a");
    a.href = outputImage.src;
    a.download = "processed.png";
    a.click();
});


// ------------------ Initialize ------------------
hideAllParams();
