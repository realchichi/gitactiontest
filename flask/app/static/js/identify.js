var imageData = null;


const fileUpload = (event) => {
    const files = event.target.files;
    const filesLength = files.length;
        if (filesLength > 0) {
            imageData = URL.createObjectURL(files[0]); 
            const imagePreviewElement = document.querySelector("#photo");
            imagePreviewElement.src = imageData;
            imagePreviewElement.style.display = "block";

        }
    };


document.addEventListener('DOMContentLoaded', () => {
  var width = 320;
  var height = 0;
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
            imageData = canvas.toDataURL('image/jpeg');
            const imagePreviewElement = document.querySelector("#photo");
            imagePreviewElement.src = imageData;
            imagePreviewElement.style.display = "block";

        });
        closeCam.addEventListener('click', () => {
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(track => track.stop());
                video.srcObject = null;
                closePopup()
            }
        });

    });

});

function identifyImage() {
  if (imageData) {
    const formData = new FormData();
    formData.append('image', imageData);
    // console.log("FormData Content:");
    // for (const pair of formData.entries()) {
    //     console.log(pair[0] + ': ' + pair[1]);
    // }
    fetch('/identification', {
       method: 'POST',
       headers: {
        'Content-Type': 'application/json',
      },
       body: formData,
     })
     .then(response => response.json())
     .then(data => {
         console.log('Identification results:', data);
     })
     .catch(error => {
         console.error('Error identifying image:', error);
         // Handle the error appropriately, e.g., show a user-friendly message
     });
    }
}

function openPopup() {
    // Show the overlay and modal
    document.getElementById('modal').style.display = 'block';

    }


function closePopup() {
    // Hide the overlay and modal
    document.getElementById('modal').style.display = 'none';
    }