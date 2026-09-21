from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove, new_session

app = FastAPI()

# 4MB-র u2netp মডেল যা 512MB RAM-এ নিরাপদভাবে চলে
session = new_session("u2netp")

@app.get("/")
def home():
    return {"status": "AI Background Remover API is Running"}

@app.post("/remove-bg")
async def remove_bg(image_file: UploadFile = File(...)):
    try:
        input_bytes = await image_file.read()
        if not input_bytes:
            raise HTTPException(status_code=400, detail="No image data received")

        output_bytes = remove(input_bytes, session=session)
        return Response(content=output_bytes, media_type="image/png")
    except Exception as e:
        return Response(content=f"Python Execution Error: {str(e)}", status_code=500)
