document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('camera-preview');
    const canvas = document.getElementById('canvas');
    const captureBtn = document.getElementById('capture-btn');
    var constraints = { video: false };
    const closeCam = document.getElementById("close-cam")
    const openCam = document.getElementById("open-cam")
    let stream = null;


    openCam.addEventListener("click", () => {
      constraints = {video : true};

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

        const imageDataURL = canvas.toDataURL('image/jpeg');
        const blob = dataURLtoBlob(imageDataURL);

        const formData = new FormData();
        formData.append('image', blob, 'captured_image.jpg');

        fetch('/identification', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(message => console.log(message))
        .catch(error => console.error('Error uploading image:', error));
    });
    closeCam.addEventListener('click', () => {
       
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            video.srcObject = null;
        }
    });

    function dataURLtoBlob(dataURL) {
        const parts = dataURL.split(';base64,');
        const contentType = parts[0].split(':')[1];
        const byteCharacters = atob(parts[1]);
        const byteArrays = new Array(byteCharacters.length);

        for (let i = 0; i < byteCharacters.length; i++) {
            byteArrays[i] = byteCharacters.charCodeAt(i);
        }

        return new Blob([new Uint8Array(byteArrays)], { type: contentType });
    }
    });

});