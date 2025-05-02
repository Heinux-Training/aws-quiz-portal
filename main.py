from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional  # Import typing utilities for type annotations
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware to handle cross-origin requests
import format # Import the format module, which contains the logic for generating quizzes
import boto3
import os
import json

app = FastAPI(title="Quiz Generator API")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,  # Allow credentials (e.g., cookies, authorization headers)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the request model for the /generate-questions endpoint
class QuizRequest(BaseModel):
    cert_name: str  # e.g., AWS Solutions Architect
    difficulty: int = 2  # Default difficulty level 
    num_questions: int = 3  # Default number of questions

# Define the model for a single quiz question
class Question(BaseModel):
    question: str  # The text of the question
    options: List[str]  # A list of answer options
    answer: str  # The correct answer
    explanation: str  # An explanation for the correct answer

# Define the response model for the /generate-quiz endpoint
class QuizResponse(BaseModel):
    questions: List[Question]  # A list of questions in the quiz

# Configure Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

@app.post("/generate-questions")
async def generate_questions(request: QuizRequest):
    try:
        # Call the format.get_quiz function to generate quiz data
        quiz_json = format.get_quiz(
            cert_name=request.cert_name,  # Pass the certificate name from the request
            difficulty=request.difficulty,  # Pass the difficulty level
            num_questions=request.num_questions  # Pass the number of questions
        )
        
        # Parse the JSON string returned by format.get_quiz()
        quiz_data = json.loads(quiz_json)
        
        # The data structure is {"questions": {"questions": [...]}}
        # Restructure it to match the expected response model
        if "questions" in quiz_data and "questions" in quiz_data["questions"]:
            return {"questions": quiz_data["questions"]["questions"]}
        else:
            # Handle case where the response structure is unexpected
            raise HTTPException(status_code=500, detail="Unexpected response structure from quiz generator")
            
    except Exception as e:
        # Handle any exceptions and return a 500 error with the exception message
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

# Define a health check endpoint to verify the API is running
@app.get("/")
async def health_check():
    return {"status": "healthy"}  # Return a simple JSON response indicating the API is healthy      