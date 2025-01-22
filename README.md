YouTube Comment Sentiment Analysis
This is a Streamlit app that allows you to analyze the sentiment of comments from any YouTube video. The app fetches comments from a YouTube video using the YouTube Data API, translates the comments to English (if necessary), classifies their sentiment, and provides insightful visualizations and metrics.

Features:
Fetches comments from a YouTube video.
Translates non-English comments to English.
Classifies comments into categories like Appreciation, Constructive Feedback, Negative Criticism, Question/Inquiry, Spam/Promotional, and Neutral Statements.
Displays the sentiment distribution in a pie chart.
Visualizes the likes distribution across different sentiment categories.
Provides a sentiment timeline showing how sentiment evolves over time.
Allows the user to download the results as a CSV file.
Prerequisites:
Python 3.x installed on your local machine.
Streamlit for the web interface.
Google API Key from Google Cloud Console for accessing the YouTube Data API.
Installation Instructions:
Clone the repository or download the script file:

bash
Copy
Edit
git clone https://github.com/your-repository/YouTube-Comment-Sentiment-Analysis.git
Install dependencies using pip:

bash
Copy
Edit
pip install streamlit google-api-python-client pandas numpy textblob deep-translator plotly
Get a YouTube Data API key:

Go to Google Cloud Console.
Create a new project (or select an existing one).
Enable the YouTube Data API v3.
Generate an API key for your project.
Run the app: In the terminal, navigate to the folder where the app script is located and run:

bash
Copy
Edit
streamlit run youtube_comment_analysis.py
Access the app: Open your browser and go to http://localhost:8501 to view the app.

Usage:
Enter API Key: In the sidebar, enter your YouTube API key.
Enter Video URL: Paste the YouTube video URL in the input field.
Select Maximum Comments: Choose the maximum number of comments to analyze (default is 100).
Click "Analyze Comments": The app will fetch the comments, translate them (if necessary), classify their sentiment, and generate visualizations.
View Results:
Visualizations: Sentiment distribution, likes distribution, and sentiment timeline.
Comments Table: See the comments along with their sentiment and like count.
Raw Data: View the raw JSON data of the fetched comments.
Download Results: Click the "Download Analysis Results" button to download the analysis as a CSV file.
Components:
Sentiment Classification: Uses simple keyword matching along with TextBlob sentiment analysis for more nuanced classification.
Translation: Uses the deep_translator library to translate non-English comments to English.
Visualization: Utilizes Plotly for generating interactive visualizations of sentiment distribution, likes distribution, and sentiment over time.
Example:

Limitations:
The app fetches a maximum of 500 comments per video.
The sentiment classification is based on predefined keywords and may not be perfect for every comment.
The translation is limited to the capabilities of the Google Translate API.
Contributions:
Feel free to fork the repository and submit pull requests for improvements, bug fixes, or new features. If you find a bug, open an issue on GitHub, and we will address it as soon as possible.

License:
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements:
YouTube Data API v3
Streamlit
Plotly
TextBlob
Deep Translator
