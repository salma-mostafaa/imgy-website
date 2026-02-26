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
const inputImage = document.getElementById("inputImage");
const resetBtn = document.getElementById("resetBtn");
const downloadBtn = document.getElementById("downloadBtn");

let originalFile = null; 
let originalImageSrc = null;

function hideAllParams() {
    logBox.style.display = "none";
    translateBox.style.display = "none";
    rotateBox.style.display = "none";
    bitBox.style.display = "none";
    cannyBox.style.display = "none";
    shearBox.style.display = "none";
}

operationSelect.addEventListener("change", () => {
    hideAllParams();
    const op = operationSelect.value;
    if (op === "log" || op === "inv_log") logBox.style.display = "block";
    else if (op === "translate") translateBox.style.display = "block";
    else if (op === "rotate") rotateBox.style.display = "block";
    else if (op === "bit_plane") bitBox.style.display = "block";
    else if (op === "canny") cannyBox.style.display = "block";
    else if (op === "shear") shearBox.style.display = "block";
});

imageInput.addEventListener("change", (e) => {
    originalFile = e.target.files[0];
    if (!originalFile) return;

    const reader = new FileReader();
    reader.onload = () => {
    inputImage.src = reader.result;     
    originalImageSrc = reader.result;
};

    reader.readAsDataURL(originalFile);
});

uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!originalFile) {
        alert("Please upload an image first!");
        return;
    }

    const formData = new FormData();
    formData.append("image", originalFile);

    const image2 = document.getElementById("image2").files[0];
    if (image2) formData.append("image2", image2);

    formData.append("operation", operationSelect.value);

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
    } else if (operationSelect.value === "shear") {
        formData.append("shx", document.getElementById("shx").value);
        formData.append("shy", document.getElementById("shy").value);
    }

    try {
        const response = await fetch(`${window.location.origin}/process`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        outputImage.src = data.image;

        const res = await fetch(data.image);
        const blob = await res.blob();
        originalFile = new File([blob], "processed.png", { type: "image/png" });

    } catch (err) {
        console.error(err);
        alert("Error processing image");
    }
});

resetBtn.addEventListener("click", () => {
    fetch(`${window.location.origin}/reset`, { method: "POST" })
        .then(() => {
            if (originalImageSrc && imageInput.files[0]) {
                inputImage.src = originalImageSrc;
                outputImage.src = "";
                originalFile = imageInput.files[0];
            }
        })
        .catch(err => console.error(err));
});


downloadBtn.addEventListener("click", () => {
    if (!outputImage.src) {
        alert("No image to download");
        return;
    }
    const a = document.createElement("a");
    a.href = outputImage.src;
    a.download = "processed.png";
    a.click();
});

hideAllParams();
