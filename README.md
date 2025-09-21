# HACKATHON RESUME CHECKER
Your original code organized into files. Run with streamlit run app.py
Sample data: Unzipped JD.zip and Resumes.zip into /content/sample_data/jds/ and /content/sample_data/resumes/.
# AI Resume Relevance Checker

**Built for Code4EdTech Hackathon Challenge by Innomatics**

An AI-powered web application to analyze resumes against job descriptions (JDs), providing relevance scores, skill matches, and improvement suggestions. Designed for placement and recruiting teams to streamline candidate evaluation.

## 🎯 Project Overview

The AI Resume Relevance Checker leverages natural language processing (NLP) to compare resumes (PDF/DOCX) with job descriptions (PDF or text). It calculates a relevance score, identifies matched/missing skills, and offers tailored suggestions. Built with Streamlit, the app features a Dashboard for reviewing past analyses, making it ideal for recruiters during hiring drives.

Developed for the Code4EdTech Hackathon Challenge by Innomatics , this tool combines AI-driven analysis with a user-friendly interface, supporting 10 sample resumes and 2 JDs.

## ✨ Features

### Resume Analysis
- Upload resumes (PDF/DOCX) or select from 10 samples
- Input JDs (text or PDF) or choose from 2 samples
- AI analysis using sentence-transformers for relevance scoring
- Displays score (0-100%), verdict (Strong/Moderate/Weak), skills, and suggestions
- Interactive gauge chart for scores
- Download results as JSON
![resumeanalysis](https://github.com/user-attachments/assets/d8949f52-d0da-41b6-b0da-f28a9f9ab7d4)

### Dashboard
- Table of all analyses (Resume, JD Source, Score, Verdict, Skills, Date)
- Download all analyses as JSON
- ![dashboard](https://github.com/user-attachments/assets/f854b556-b4e3-4d1e-986c-794bcfcc7dc7)


### Polished UI
- Custom Streamlit theme with green/blue buttons and hover effects
- Sidebar with Analysis/Dashboard tabs and sample selectors
- Progress bar for analysis
- ![resumechecker](https://github.com/user-attachments/assets/6bcaa8f9-fc53-4a15-af99-f083ba8f546e)

### Sample Data
- 10 resumes in `sample_data/resumes/Resumes/` (PDFs, DOCX)
- 2 JDs in `sample_data/jds/JD/` (PDFs)

## 🛠 Setup Instructions

### Prerequisites
- Python 3.8+
- Git
- Streamlit Cloud account
- Dependencies (requirements.txt):
  ```
  streamlit
  PyPDF2
  python-docx
  sentence-transformers
  plotly
  pandas
  scikit-learn
  ```

### Local Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Tanishtha-Reddy/AI-Resume-Analyzer-for-Hackathon.git
   cd AI-Resume-Analyzer-for-Hackathon
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Access at:** http://localhost:8501

### Streamlit Cloud Deployment

1. Sign in to [share.streamlit.io](https://share.streamlit.io) with GitHub
2. Create app:
   - Repository: `Tanishtha-Reddy/AI-Resume-Analyzer-for-Hackathon`
   - Branch: `main`
   - Main file path: `app.py`
3. Deploy and access the URL (e.g., https://yourappname.streamlit.app)

## 🚀 Usage

### 1. Analysis Tab
- Select/upload a resume (PDF/DOCX)
- Select/paste/upload a JD (text/PDF)
- Click "Analyze Resume" for:
  - Relevance score, verdict, skills, suggestions
  - JSON download

### 2. Dashboard Tab
- View analysis history table
- Download all analyses as JSON

### 3. Sample Data
- Test with 10 resumes and 2 JDs in `sample_data/`

## 📂 File Structure

```
AI-Resume-Analyzer-for-Hackathon/
├── app.py                    # Main Streamlit app
├── utils/                    # Helper modules
│   ├── parsing.py            # Text extraction
│   ├── matching.py           # Skill matching
│   ├── scoring.py            # Relevance scoring
│   └── visualization.py      # Gauge chart
├── .streamlit/               # Theme config
│   └── config.toml
├── sample_data/              # Sample data
│   ├── resumes/Resumes/      # 10 resumes
│   └── jds/JD/               # 2 JDs
├── analysis_history.json     # Analysis results
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
└── .gitignore                # Git ignore
```

## 💡 Notes

- **Analysis History:** Stored in `analysis_history.json` locally. Persistent storage (e.g., SQLite) can be added.
- **Demo Tip:** Run live analyses to populate the Dashboard for judges.

## 🙌 Credits

- **Developer's team:** Pranavi,Tanishtha,Nikitha
- **College Name:** Marri Laxman Reddy Institute of Technology And Management
- **AI Model:** sentence-transformers/all-MiniLM-L6-v2
- **Framework:** Streamlit
- **Hackathon:** Code4EdTech Hackathon Challenge by Innomatics
## 🎉 Conclusion
The AI Resume Relevance Checker demonstrates the power of combining modern AI technologies with intuitive user interfaces to solve real-world recruitment challenges. Built during the intense 24-hour hackathon timeframe, this application successfully bridges the gap between manual resume screening and automated candidate evaluation.
By leveraging sentence transformers and natural language processing, the tool provides recruiters with objective, data-driven insights that can significantly speed up the hiring process while maintaining accuracy. The comprehensive dashboard and analysis features make it a practical solution for placement teams handling large volumes of applications.
This project showcases how AI can be democratized and made accessible through simple web interfaces, enabling non-technical users to harness sophisticated machine learning capabilities for their daily workflows.

