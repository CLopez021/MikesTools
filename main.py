from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import assemblyai as aai
import os
import tempfile
from dotenv import load_dotenv
import uuid
import atexit
import shutil
from utils import generate_srt

load_dotenv()
app = FastAPI()

# Replace with your chosen API key
aai.settings.api_key = os.getenv("ASSEMBLY_AI_API_KEY")

# Create tmp directory for SRT files
TMP_DIR = os.path.join(tempfile.gettempdir(), "srt_files")
os.makedirs(TMP_DIR, exist_ok=True)

def cleanup_tmp_dir():
    """Clean up tmp directory on server shutdown"""
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
        
# Register cleanup function
atexit.register(cleanup_tmp_dir)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML page"""
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Upload an audio file and transcribe it using AssemblyAI
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Configure transcription settings
        config = aai.TranscriptionConfig(
            speaker_labels=True,
            format_text=True,
            punctuate=True,
            speech_model=aai.SpeechModel.best,
            language_detection=True
        )
        
        # Transcribe the audio file
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(temp_file_path)
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        # Check for errors
        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(status_code=500, detail=transcript.error)
        
        # Generate SRT content
        srt_content = generate_srt(transcript)
        
        # Save SRT file to tmp directory
        file_id = str(uuid.uuid4())
        srt_filename = f"{file_id}.srt"
        srt_path = os.path.join(TMP_DIR, srt_filename)
        
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        # Return the transcription result
        return JSONResponse(content={
            "success": True,
            "text": transcript.text,
            "language_code": transcript.language_code if hasattr(transcript, 'language_code') else None,
            "srt_file_id": file_id,
            "srt_filename": f"{os.path.splitext(file.filename)[0]}.srt"
        })
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_id}")
async def download_srt(file_id: str):
    """
    Download the generated SRT file
    """
    srt_path = os.path.join(TMP_DIR, f"{file_id}.srt")
    
    if not os.path.exists(srt_path):
        raise HTTPException(status_code=404, detail="SRT file not found")
    
    return FileResponse(
        path=srt_path,
        media_type="application/x-subrip",
        filename=f"{file_id}.srt"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

