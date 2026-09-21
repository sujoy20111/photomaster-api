from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove, new_session
import io

app = FastAPI()

# 4MB-র অতি হালকা মডেল যা 512MB RAM-এ কোনো ক্র্যাশ ছাড়া চলবে
session = new_session("u2netp")

@app.post("/remove-bg")
async def remove_background(image_file: UploadFile = File(...)):
    try:
        # ফাইল রিড করা
        contents = await image_file.read()
        
        # u2netp সেশন দিয়ে ব্যাকগ্রাউন্ড রিমুভ (অল্প র‍্যামে দ্রুত কাজ করে)
        output_image = remove(contents, session=session)
        
        return Response(content=output_image, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
