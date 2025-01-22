import streamlit as st
import os
from googleapiclient.discovery import build
import pandas as pd
import numpy as np
from textblob import TextBlob
from deep_translator import GoogleTranslator
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import time

# Set page config
st.set_page_config(
    page_title="YouTube Comment Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #1DA1F2;
    }
    .sentiment-metric {
        font-size: 24px;
        font-weight: bold;
        color: #1DA1F2;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper Functions
def create_youtube_service(api_key):
    """Create YouTube service object"""
    return build('youtube', 'v3', developerKey=api_key)

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    if "v=" in url:
        return url.split("v=")[1][:11]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1][:11]
    return url[:11]

def get_video_comments(service, video_id, max_results=100):
    """Fetch comments from a YouTube video"""
    comments = []
    try:
        request = service.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_results,
            textFormat='plainText'
        )
        
        with st.progress(0) as progress_bar:
            while request and len(comments) < max_results:
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likes': comment['likeCount'],
                        'published_at': comment['publishedAt']
                    })
                
                progress_bar.progress(min(len(comments) / max_results, 1.0))
                request = service.commentThreads().list_next(request, response)
                
        return comments
    except Exception as e:
        st.error(f"Error fetching comments: {str(e)}")
        return []

def translate_text(text, target_lang='en'):
    """Translate text to target language"""
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except:
        return text

def classify_sentiment(text):
    """Classify comment sentiment based on defined criteria"""
    text_lower = text.lower()
    
    # Keyword-based classification
    if any(word in text_lower for word in ['amazing', 'great', 'awesome', 'loved', 'excellent', 'thanks', 'thank you']):
        return 'Appreciation'
    elif any(word in text_lower for word in ['could be', 'should', 'suggest', 'improve', 'better if']):
        return 'Constructive Feedback'
    elif any(word in text_lower for word in ['terrible', 'waste', 'worst', 'horrible', 'bad', 'awful']):
        return 'Negative Criticism'
    elif any(word in text_lower for word in ['?', 'how', 'what', 'when', 'where', 'why', 'can you']):
        return 'Question/Inquiry'
    elif any(word in text_lower for word in ['subscribe', 'check out', 'visit', 'follow', 'my channel']):
        return 'Spam or Promotional'
    else:
        # TextBlob sentiment analysis for nuanced classification
        sentiment = TextBlob(text).sentiment.polarity
        if abs(sentiment) < 0.1:
            return 'Neutral Statements'
        elif sentiment > 0:
            return 'Appreciation'
        else:
            return 'Negative Criticism'

# Visualization Functions
def create_sentiment_distribution(df):
    """Create sentiment distribution pie chart"""
    sentiment_counts = df['sentiment'].value_counts()
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title='Distribution of Comment Sentiments',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

def create_likes_distribution(df):
    """Create likes distribution box plot"""
    fig = px.box(
        df,
        x='sentiment',
        y='likes',
        title='Likes Distribution by Sentiment',
        color='sentiment',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

def create_sentiment_timeline(df):
    """Create sentiment timeline"""
    df['published_at'] = pd.to_datetime(df['published_at'])
    timeline_data = df.groupby([df['published_at'].dt.date, 'sentiment']).size().unstack(fill_value=0)
    
    fig = px.line(
        timeline_data,
        title='Sentiment Timeline',
        labels={'value': 'Number of Comments'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

# Main App
def main():
    st.title("📊 YouTube Comment Sentiment Analysis")
    st.write("Analyze sentiment of comments on any YouTube video")
    
    # Sidebar
    st.sidebar.header("Settings")
    api_key = st.sidebar.text_input("Enter YouTube API Key", type="password")
    max_comments = st.sidebar.slider("Maximum comments to analyze", 10, 500, 100)
    
    # Main content
    video_url = st.text_input("Enter YouTube Video URL")
    
    if st.button("Analyze Comments") and api_key and video_url:
        try:
            with st.spinner("Fetching and analyzing comments..."):
                # Create YouTube service
                service = create_youtube_service(api_key)
                video_id = get_video_id(video_url)
                
                # Get comments
                comments = get_video_comments(service, video_id, max_comments)
                
                if comments:
                    # Create DataFrame
                    df = pd.DataFrame(comments)
                    
                    # Translate and classify
                    with st.spinner("Translating and classifying comments..."):
                        df['translated_text'] = df['text'].apply(lambda x: translate_text(x))
                        df['sentiment'] = df['translated_text'].apply(classify_sentiment)
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Comments", len(df))
                    with col2:
                        st.metric("Positive Sentiment", 
                                len(df[df['sentiment'].isin(['Appreciation', 'Constructive Feedback'])]))
                    with col3:
                        st.metric("Negative Sentiment",
                                len(df[df['sentiment'] == 'Negative Criticism']))
                    
                    # Create tabs for different views
                    tab1, tab2, tab3 = st.tabs(["📊 Visualizations", "📝 Comments Table", "📈 Raw Data"])
                    
                    with tab1:
                        # Visualizations
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(create_sentiment_distribution(df), use_container_width=True)
                        with col2:
                            st.plotly_chart(create_likes_distribution(df), use_container_width=True)
                        
                        st.plotly_chart(create_sentiment_timeline(df), use_container_width=True)
                    
                    with tab2:
                        # Display interactive table
                        st.dataframe(
                            df[['author', 'text', 'sentiment', 'likes']]
                            .sort_values('likes', ascending=False),
                            use_container_width=True
                        )
                    
                    with tab3:
                        # Display raw data
                        st.json(comments)
                    
                    # Allow CSV download
                    st.download_button(
                        label="Download Analysis Results",
                        data=df.to_csv(index=False).encode('utf-8'),
                        file_name='youtube_comment_analysis.csv',
                        mime='text/csv'
                    )
                else:
                    st.warning("No comments found for the video.")
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    # Instructions
    with st.expander("How to Use"):
        st.write("""
        1. Get a YouTube Data API key from Google Cloud Console
        2. Enter your API key in the sidebar
        3. Paste a YouTube video URL
        4. Click 'Analyze Comments'
        5. View the results in different tabs
        6. Download the analysis results as CSV
        """)

if __name__ == "__main__":
    main()