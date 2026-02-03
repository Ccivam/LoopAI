from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import tempfile
import os

# Import your modules
from voice.stt import speech_to_text
from voice.tts import speak_to_file
from rag.retriever import retrieve
from rag.prompt import build_prompt
from llm.gemini_client import ask_gemini

app = FastAPI()

# Serve frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
@app.get("/intro")
def intro():
    intro_text = "Hello, I am Loop AI, your hospital network assistant."
    audio_path = speak_to_file(intro_text)
    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename="intro.wav"
    )

# Serve index.html at root
@app.get("/")
def read_index():
    return FileResponse("frontend/index.html")

# Keep conversation memory for follow-ups
conversation_memory = []

@app.post("/voice")
async def voice_endpoint(audio: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        audio_path = tmp.name

    # Convert speech to text
    query = speech_to_text(audio_path)
    os.remove(audio_path)

  
    

    # Retrieve hospital info
    results = retrieve(query)
   
    if not results:
        response_text = (
            "I'm sorry, I can't help with that. "
            "I am forwarding this to a human agent."
        )
    else:
        # Build prompt including conversation history for follow-ups
        #prompt = build_prompt(results, query, conversation_memory)
        #response_text = ask_gemini(prompt)
        response_text=results

    # Save conversation
   
    conversation_memory.append({"role": "user", "content": query})
    conversation_memory.append({"role": "assistant", "content": response_text})

    # Generate audio response
    audio_response_path = speak_to_file(response_text)

    return FileResponse(
        audio_response_path,
        media_type="audio/wav",
        filename="response.wav"
    )
