# NLP Similarity Checks
This repo contains a few different methods to check the similarity between two phrases. A flask server ``server.py`` can be run to take in values and respond with the similarity.

There is also some code for negation. I was finding that some concepts were confusing the NLP models if they were opposites. For example, trying to compare the phrases
```
The patient smokes once a day.
```
and
```
The patient has never smoked.
```
would spit out a high confidence level that these were the same concepts. As a team, we decided to implement negation to eliminate these negative concepts entirely so that our lives will be simpler.


## Current Operation
This is how the programs currently interact.

1. Client makes a request to ``server.py`` 
    - There are currently 2 routes they can call: ``/getsimilarity`` and ``/negation``
2. These routes call functions defined in the other files.
    - ``/getsimilarity`` sends two strings to ``getSimilarity()`` in ``biobert.py`` 
    - ``/negation`` sends whatever data it is passed to ``execNegation()`` in ``negation.py``
3. When the data is processed and ready to go, it is returned to the client.

The files can be run on their own with hard coded values if desired, however some of the functions that run this way have been commented out or deleted. They would need to be enabled/created to allow them to function this way. 


## The Vision
The way this should work in the end is that a frontend will make a request to the an API to retrieve patient data. The API will retrieve the data, and any other data needed for processing and then send both of those off to be negated. Once they are both negated, they will be sent off to be compared. The comparison will work by assuming similarities based on confidence levels. Let's say that the comparison model is 75% confident that the 2 concepts it analyzed were similar. If that confidence level is over our determined confidence threshold (TBD), it will set a ``similar`` flag in the data. Once all of that is complete, it will return the resulting data to the frontend to be displayed to the user.

One thought I have, is that I would like to exploring loading statuses with this. These comparisons can take anywhere from 10 - 20 seconds per patient, so it would be nice to let the user know how far along in the process it is. I am not sure how this would work exactly with NLP because you would need to somehow calculate a completion percentage. I recently watched a video on "Server Side Events" and websockets. Both seem like good options to send status updates to the frontend. 
