var imageData = {};

function fileUpload(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var dataURL = reader.result;

        var photo = document.getElementById('photo');
        photo.src = dataURL;

    };

    reader.readAsDataURL(input.files[0]);
    imageData = reader;
}

document.addEventListener('DOMContentLoaded', () => {
    var width = 320;
    var height = 0;
    const video = document.getElementById('camera-preview');
    const canvas = document.getElementById('canvas');
    const captureBtn = document.getElementById('capture-btn');
    var constraints = { video: false };
    const closeCam = document.getElementById("close-cam");
    const openCam = document.getElementById("open-cam");
    let stream = null;

    openCam.addEventListener("click", () => {
        constraints = { video: true };

        navigator.mediaDevices.getUserMedia(constraints)
            .then((mediaStream) => {
                video.srcObject = mediaStream;
                stream = mediaStream;
            })
            .catch((err) => {
                console.error('Error accessing camera:', err);
            });

        captureBtn.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            imageData = { "result": canvas.toDataURL('image/jpeg') };
            const imagePreviewElement = document.querySelector("#photo");
            imagePreviewElement.src = imageData["result"];
            imagePreviewElement.style.display = "block";
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(track => track.stop());
                video.srcObject = null;
                closePopup();
            }
            closePopup();
        });

        closeCam.addEventListener('click', () => {
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(track => track.stop());
                video.srcObject = null;
                closePopup();
            }
        });

        // Drag and drop functionality// if do not use just delete it 
        const dropZone = document.getElementById('drop-zone');

        dropZone.addEventListener('dragover', (event) => {
            event.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (event) => {
            event.preventDefault();
            dropZone.classList.remove('drag-over');
            const file = event.dataTransfer.files[0];
            handleDrop(file);
        });

    });

});

function handleDrop(file) {
    const reader = new FileReader();
    reader.onload = function () {
        const dataURL = reader.result;
        const photo = document.getElementById('photo');
        photo.src = dataURL;
    };
    reader.readAsDataURL(file);
    imageData = reader;
}

function openPopup() {
    document.getElementById('modal').style.display = 'block';
}

function closePopup() {
    document.getElementById('modal').style.display = 'none';
}

$("#plant-img").submit(function (event) {
    event.preventDefault();
    var formData = null;

    if ("result" in imageData) {
        formData = { "image": imageData["result"] };
    } else {
        formData = { "image": imageData };
    }

    var url = "/identification";
    $.post(url, formData, function (data) {
        console.log(data);
        window.location.href = "/result?plant_data=" + data["identified_plant"];
    });
});
