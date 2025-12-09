# Welcome to our data science project: The Librarian
### Recommending media for politics and computer science topics!

### Authors: Manas Goswami & Prakrati Kadekar

## How to use:

### Python Necessery Libraries:
- pandas
- sentence_transformers
- re (built-in)
- numpy
- kaggle
- kagglehub
- time (built-in)
- os (built-in)
- python-dotenv
- google-api-python-client

### Other Necessery Downloads:
- npm

### Running the Project:
1. First create a youtube API key via console.cloud.google.com. Then paste your API key in api.env in YOUTUBE_API_KEY.
2. Do the same thing with kaggle api key gotten by going to your kaggle profile, clicking settings, going to account, then scrolling down to API. Paste your API key in api.env in KAGGLE_KEY.
3. In KAGGLE_USERNAME paste your kaggle username.
4. Open up 2 terminals
5. In the first terminal run python main.py
6. In the second one, cd into the librarian-ui directory
7. Then in the second terminal run npm install
8. Then run npm run dev
9. Wait for both terminals to finish loading. The first terminal should show that debugger is active. The second terminal should show a local host that you can visit.
10. Then load the local host website on your browser. Now you can search up a political or tech topic you want to learn about

