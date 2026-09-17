from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import new_session, remove

app = FastAPI()
session = new_session("u2netp")

@app.get("/")
def health():
    return {"status": "running", "service": "PhotoMaster BG Remover"}

@app.post("/remove-bg")
async def remove_bg(image_file: UploadFile = File(...)):
    try:
        data = await image_file.read()
        result = remove(data, session=session)
        return Response(content=result, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
