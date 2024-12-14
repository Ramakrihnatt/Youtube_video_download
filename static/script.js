const form = document.getElementById('download-form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const videoLink = document.getElementById('video-link').value;
    const statusMessage = document.getElementById('status-message');
    statusMessage.textContent = "Processing... Please wait.";

    try {
        // Make a POST request to download the video
        const response = await fetch('http://localhost:8000/download', {
            method: 'POST',
            body: new URLSearchParams({ link: videoLink }) // Send link as form data
        });

        const data = await response.json();

        if (data.status === "Download started") {
            const fileId = data.file_id;

            // After the download starts, create a link to fetch the file
            const downloadLink = document.createElement('a');
            downloadLink.href = `http://localhost:8000/download/${fileId}`; // Using the file ID to get the video
            downloadLink.download = `video-${fileId}.mp4`; // Set the filename
            downloadLink.click();

            statusMessage.textContent = "Download started! Video will be saved to your browser's download location.";
        } else {
            statusMessage.textContent = "Error: Unable to start download.";
        }
    } catch (error) {
        statusMessage.textContent = `Error: ${error.message}`;
    }
});
