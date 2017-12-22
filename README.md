# Filmoji

![Filmoji](static/img/logo.png)

<br/>

Mapping Hollywood Celebrities to Emojis based on their Movie Names :heart_eyes:

## Method

Started with collecting 100 Hollywood celebrities and their movies. All the movie names then converted to **word vectors** using **word2vec**(Google News 2014). For each movie, a dictionary of emojis is generated with similarity. Similarity is calculated using cosine similar with the help of vector representation of emojis (**emoji2vec**). Then for each actor, all of the dictionaries are merged together with the summation of similarity scores. From this combined dictionary, top 10 emojis are selected and visualized.

-> Since some movie names do not exist in English vocabulary, they couldn't be considered to generate the emojis.

## Libraries Used

* Pandas :panda_face:
* Gensim :gift:
* NumPy :1234:
* SciPy :space_invader:
* num2words :abcd:
* imdb :movie_camera:

### Special Thanks

Special Thanks to @PableraShow for the [amazing table template](https://codepen.io/PableraShow/pen/qdIsm)