from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI()

# 4MB-র অতি হালকা মডেল যা কখনোই 512MB RAM অতিক্রম করবে না
session = new_session("u2netp")

@app.post("/remove-bg")
async def remove_background(image_file: UploadFile = File(...)):
    try:
        # ফাইল রিড করা
        input_data = await image_file.read()
        
        # PIL দিয়ে ইমেজ খোলা ও মেমোরি অপটিমাইজেশন
        img = Image.open(io.BytesIO(input_data))
        
        # ছবি বেশি বড় হলে সাময়িকভাবে সাইজ ছোট করা (মেমোরি ক্র্যাশ ঠেকাতে)
        max_dimension = 1500
        if max(img.size) > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            input_data = buffer.getvalue()

        # ব্যাকগ্রাউন্ড রিমুভ করা
        output_bytes = remove(input_data, session=session)
        
        return Response(content=output_bytes, media_type="image/png")
        
    except Exception as e:
        return Response(content=str(e), status_code=500)
