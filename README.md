# houndify-keyphrase-spotting

This uses houndify's api to respond to voice queries. On top of that is has keyphrase detection. This means that you can create custom propts such as "ok hound" to start the queries.

# How To
Run the program using: 
```
python keywordDetector.py <your_houndify_key> <your_houndify_id>
```
To modify the keyphrase change the string on the right hand side of `decoder.set_keyphrase` in keywordDetector.py

# Notes
Response dictation is not great right now and only works on mac. 
