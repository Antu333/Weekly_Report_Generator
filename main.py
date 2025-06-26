from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

YOUR_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=YOUR_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Initialize FastAPI app
app = FastAPI(title="Weekly Report Generator (Gemini)", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for input
class ReportRequest(BaseModel):
    project_name: str
    time_period: str
    completed: str
    ongoing: str
    upcoming: str
    issues: str
    tone: str

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/", response_class=FileResponse)
def serve_home():
    return FileResponse("frontend/index.html")
# POST endpoint
@app.post("/generate-report")
def generate_report(req: ReportRequest):
    try:
        tone_instruction = (
    "Use a friendly, slightly casual tone. Be human and conversational."
    if req.tone == "casual"
    else "Use a formal and professional tone suitable for corporate communication."
)
        prompt = f"""
You are an AI assistant writing a friendly and professional weekly status report for the project: {req.project_name}.

Write a narrative-style report for the period: {req.time_period}

Here are the bullet points:
- ✅ Tasks completed: {req.completed}
- 🔄 Ongoing tasks: {req.ongoing}
- 🗓️ Upcoming tasks: {req.upcoming}
- ⚠️ Issues faced: {req.issues}

Instructions:
- Use the following tone: {tone_instruction}.
- Make it sound like a real person wrote it.
- Use a friendly but formal tone.
- Break the report into 4 sections with bold headings.
- Add light transitions between sections so it flows naturally.
- End with a positive, forward-looking sentence.
- Give a report summary at the end.
- give key takeaways at the end.
"""

        response = model.generate_content(prompt)
        return {"report": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
