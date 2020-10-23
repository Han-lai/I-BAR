## I-BAR,the AI Bartender

###### You know that thing  When you walk into a bar full of mystery, the bartender asks you what you'd like to have—not in terms of a specific cocktail, or even the base spirit, but in terms of the flavor profile? And then just sets to work grabbing one bottle after another until before you know it you've got a little bit of magic in your mouth and you don't even know how? As far as I'm concerned.That's "I-BAR" experience.
###### The final goal of this project is to allow user to understand the base spirit,materials,preparation steps,etc..,so that users can learn how to create their own favorite cocktails in this project.


## Project  Process

| I-BAR         |    Process    |
| ------------- |:-------------:|
|![image](https://github.com/Han-lai/I-BAR/blob/master/01%20demo%E5%9C%96%E6%AA%94/I-BAR.png?raw=true)  |![image](https://github.com/Han-lai/I-BAR/blob/master/01%20demo%E5%9C%96%E6%AA%94/process.png?raw=true) |
## Demo - recommendation of cocktail and whisky
###### Use Line chatbot can recommend user's favorite cocktail or whisky with flavor labels 

| Cocktail      | Whisky        |
| ------------- |:-------------:|
|![image](https://github.com/Han-lai/I-BAR/blob/master/01%20demo%E5%9C%96%E6%AA%94/cocktail_demo.gif?raw=true)      |![image](https://github.com/Han-lai/I-BAR/blob/master/01%20demo%E5%9C%96%E6%AA%94/whisky.gif?raw=true)   |


## Abstract

###### The I-bar project is a cocktail and Whisky recommendation engine that built to transform plain English requests from a user into a suggested cocktail or whisky that best matches the request.

###### The functionality of this system rests on three systems:
* A database of cocktails, containing recipes, descriptions, and metadata for each.
* A model trained to vectorize and transform text describing a cocktail into an appropriate flavor space.
* Final, in this project, I focus on [collaborative filtering recommender systems](https://github.com/Han-lai/WhiskyRecommendationSystem
) since they are widely used and well research in many different business and consistently provide good business values. 

###### The text data from each cocktail is processed into a [document-term matrix](https://github.com/Han-lai/I-BAR/blob/master/TFIDF/TF-IDF_cocktail.py) using a spaCy for advanced natual language process and TF-IDF vectorizer, then factored into a document [cocktail-topic matrix](https://github.com/Han-lai/I-BAR/blob/master/kmeans/pca_kmeans_model.py) using Principal components analysis(PCA) and K-means clustering (K-means). 

###### The code for both the [I-BAR modeling](https://github.com/Han-lai/I-BAR/blob/master/kmeans/pca_kmeans_model.py) are available here, and you can read a much more in depth breakdown of how I built it on [my blog](https://hanjobs-com.webnode.tw/).


