from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import yt_dlp
import uuid

app = FastAPI()

# Enable CORS to allow cross-origin requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store the video temporarily
download_dir = "C:\\Downloads"

# Dictionary to store downloaded video filenames temporarily
downloaded_videos = {}

@app.post("/download")
async def download_video(link: str = Form(...)):
    try:
        # Generate a unique filename for the video
        unique_id = str(uuid.uuid4())  # Unique ID for the video
        filename = f"video-{unique_id}.mp4"  # Set a unique filename
        
        # Set the download options for yt-dlp
        youtube_dl_options = {
            "format": "best",
            "outtmpl": os.path.join(download_dir, filename)
        }

        # Download the video
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
        
        # Save the filename in the dictionary with the unique ID as key
        downloaded_videos[unique_id] = filename

        return {"status": "Download started", "file_id": unique_id}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error downloading video: {e}")

@app.get("/download/{file_id}")
async def get_downloaded_video(file_id: str):
    try:
        # Check if the file exists
        if file_id not in downloaded_videos:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Get the filename from the dictionary
        filename = downloaded_videos[file_id]
        file_path = os.path.join(download_dir, filename)

        # Return the file as a downloadable response
        return FileResponse(file_path, media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename={filename}"})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching video: {e}")
