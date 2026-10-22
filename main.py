from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os

app = FastAPI(title="J.A.R.V.I.S Life OS Backend")

# السماح بالاتصال من أي واجهة (Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# بيانات الاتصال بـ Supabase (تأكد من وضع مفاتيحك هنا أو في متغيرات البيئة)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://hgsifyzrugpeeqcbvuf.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "ضع_مفتاح_الـ_anon_هنا")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class MagicInputModel(BaseModel):
    user_text: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "J.A.R.V.I.S Life OS Server is running perfectly."}

@app.post("/api/process-magic")
def process_magic_input(data: MagicInputModel):
    try:
        # هنا يتم معالجة النص (أو إرساله لـ Gemini API مستقبلاً) وحفظه في جداول Supabase
        # كمثال تجريبي، سنقوم بتسجيل النص في جدول الـ daily logs أو العادات
        response = supabase.table('mental_daily_logs').insert({
            "morning_10_lines": data.user_text,
            "mood_score": 8
        }).execute()
        
        return {
            "success": True,
            "message": "تم استلام وتحليل النص وحفظه في قاعدة البيانات بنجاح!",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
