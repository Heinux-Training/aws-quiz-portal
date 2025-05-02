# aws-quiz-portal
A generative AI application that can generate quiz according to which certification and difficulty level.

## How to Run the Application

Follow the steps below to set up and run the application:

### 1. Install Requirements
Make sure you have Python installed on your system. Then, install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory of the project and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=your_openai_api_key
```

### 3. Run the backend API
Navigate to the repo root directory and run the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Run the Application
You can run the application using the following command:

```bash
streamlit run app.py
```
### 4. Access the Application
Open your web browser and go to `http://localhost:8501` to access the application.
### 5. Usage
- Select the certification you want to generate questions for.
- Choose the difficulty level.
- Click the "Generate Quiz" button.
- The generated quiz will be displayed on the screen.
### 6. Example
- Certification: AWS Certified Solutions Architect - Associate
- Difficulty Level: Medium
- Click "Generate Quiz"
- The application will generate a quiz with 5 questions related to the selected certification and difficulty level.

