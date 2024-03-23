## Instructions to use.

```
# create an .env file in your root directory.
GOOGLE_API_KEY=xxxxxxxxxxx

```
# In your root directory
source venv/bin/activate
pip install -r requirements.txt

python app.py
```

# in your root directory to create virtual environment
pip install virtualenv
virtualenv venv

source venv/bin/activate # activate virtual environment to start work
pip install -r requirements.txt

# start the application in steamlit
streamlit run app.py

```

# Some useful Google GenAI info
https://ai.google.dev/api/python/google/ai/generativelanguage/Candidate/FinishReason

# Deploy dockerized app to Google cloudrun
gcloud builds submit --tag gcr.io/cap-ragged-gem/streamlit-app --project=cap-ragged-gem
gcloud run deploy --image gcr.io/cap-ragged-gem/streamlit-app --platform managed --project=cap-ragged-gem --allow-unauthenticated

# Deploying to Heroku using Github (not dockerized)
Create ProcFile and setup.sh

# Data Scrapping using Selenium
