import csv
import json
data_list = []

with open("BtcStreamTweets(12).json") as f:
    tweets = [json.loads(line) for line in f]
    for twt in tweets:
        try:
            temp = [twt['id'], twt['user']['screen_name'], twt['user']['name'], twt['user']['url'], twt['created_at'], twt['reply_count'], twt['favorite_count'], twt['retweet_count'], twt['text']]
            data_list.append(temp)
        except:
            print("Failed")
f.close()

with open('tweets(2).csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(data_list)
file.close()
