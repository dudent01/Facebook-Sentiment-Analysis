import json
import pandas as pd
import nltk
import matplotlib.pyplot as plt

path_to_file = input("Enter the path to the chat file: ")

with open(path_to_file) as file:
    chat_history = json.load(file)

#print(chat_history)                # Display the JSON file
#print(chat_history.keys())         # Display the keys of the JSON dictionary
#print(chat_history['messages'])    # This is the information that we really want

messages = pd.DataFrame(chat_history['messages'])           # Creates pandas DataFrame for the messages
talkers  = pd.DataFrame(chat_history['participants'])


def convert_time(timestamp):
    return pd.to_datetime(timestamp, unit='ms')

messages['date'] = messages['timestamp_ms'].apply(convert_time)            # Create a date column to convert timestamp into date

def get_month(date):
    return date.month
def get_year(date):
    return date.year
def get_day(date):
    return date.day

messages['month'] = messages['date'].apply(get_month)

messages['year'] =  messages['date'].apply(get_year)

messages['day'] = messages['date'].apply(get_day)




from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sentiment_analyzer = SentimentIntensityAnalyzer()

#print(sentiment_analyzer.polarity_scores('that\'s sweet'))             # Shows the negative, neutral, positive and compound scores (compound 0 is neutral)

def get_polarity(text):                                                 # Get the compound score from text
    if (type(text) == str):                                             # Compound score is returned only when the input is a string (input is the message)
        return sentiment_analyzer.polarity_scores(text)['compound']
    return None                                                         # Otherwise, return None (will be excluded from mean computation). This happens for images and videos

#messages = messages.astype({"content": str})                            # Some of the content is float (images), need to convert everything to string
messages['sentiment'] = messages['content'].apply(get_polarity)         # Add the compound scores as a column to the DataFrame for the messages

#print(messages['sentiment'][5])            # Print the sentiment of the 5th message in the DataFrame


#averaged = messages.groupby('sender_name').mean()            # Group all rows by sender, find the average values of each column
#for i in range(len(averaged)):
#    print(averaged['sentiment'][i])
#    print('\n')


year_month = messages.groupby(['month', 'year', 'sender_name']).mean().reset_index()        # reset_index() pandas method reformats DataFrame so we can do further analysis, skipna (skip None values) is True by default


talkers_list = []
talkers_names = []
for index, row in talkers.iterrows():
    talkers_list.append(year_month[year_month['sender_name'] == row['name']]['sentiment'] .values)
    talkers_names.append(row['name'])


plt.figure(figsize= (20,10))

for person in range(len(talkers_list)):
    plt.plot(talkers_list[person], label= talkers_names[person])

plt.legend()
plt.show()