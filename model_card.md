# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Snoofy 1.0**

---

## 2. Intended Use  

The model is designed to recommend top songs to users based on their preferences for genre, mood, energy level, and acousticness. It assumes user profiles have linear preferences across these dimensions. This is still a classroom exploration project, so the recommendations are not meant for real users yet. 

---

## 3. How the Model Works  

The model works by taking a user's profile and comparing it to each song in the catalog. It calculates a score by combining the user's preferences with each song's attributes. The score is based on how well each song matches the user's preferences. The higher the score, the more likely the song is to be recommended.

---

## 4. Data  

There were initially 10 songs in the catalog, but I added 10 more songs to increase diversity. The songs represent a variety of genres (like pop, rock, jazz, classical, and electronic) and moods (like happy, sad, energetic, and calm). However, the dataset is not abundant enough to cover all musical tastes, and some genres and moods are underrepresented.

---

## 5. Strengths  

The system works well for users with clear and realistic preferences. It can recommend songs that match the user's preferred genre, mood, and energy level. The model is also able to balance multiple factors when making recommendations, which allows it to recommend songs that may not be in the user's preferred genre but have a similar mood or energy level.

---

## 6. Limitations and Bias 

The clearest weakness my experiments revealed is that energy and acousticness are
really the same signal counted twice: in this catalog they correlate at −0.97.
Because the scorer rewards a low `target_energy` and (by default) rewards
non-acoustic tracks, a user who wants calm, acoustic music is penalized on both
terms at once — one preference, two strikes. This "double jeopardy" quietly buries
acoustic genres like jazz, classical, and folk for anyone who doesn't explicitly
set `likes_acoustic=True`. In effect the model overfits to a single energy/acoustic
axis, giving genre and mood less say than the point weights suggest.

---

## 7. Evaluation  

- I tested the model using a few different user preference profiles and examined the top recommendations.  
- In recommendations, I looked for songs that matched the user's preferred genre, mood, and energy level. 
- What surprised me was that the model sometimes recommended songs that were not in the user's preferred genre, but had a similar mood or energy level.
- Some simple tests I ran were to change the user's preferred genre and see if the recommendations changed accordingly. I also tested different energy levels and acoustic preferences to see how they affected the recommendations.
- For instance, when I set the user's preferred genre to "pop" and mood to "sad", the top recommendations were mostly pop songs. But since there is no pop song in the catalog with a sad mood, it looked into the next variable, which is energy. The model recommended songs with a similar energy level to the user's preference, even if they were not in the preferred genre. This shows that the model is able to balance multiple factors when making recommendations.
---

## 8. Future Work  

- Validate & clamp inputs: clip target_energy to [0,1] and lowercase genre/mood before matching, so bad input can't hijack or silently drop matches.

- Stop double-counting energy & acousticness: since they correlate −0.97, drop one or merge them into a single "vibe" axis so calm/acoustic fans aren't penalized twice.

- Add a neutral acoustic option: replace the likes_acoustic boolean (default False) with a three-way like/dislike/don't-care so under-specified users aren't silently pushed toward electronic music.

- Use fuzzy genre/mood similarity: give partial credit for adjacent tastes ("pop"↔"indie pop", "chill"↔"relaxed") to enable discovery instead of exact-match filter bubbles.

- Score the unused features: fold valence (measured positivity) into mood matching, and use tempo_bpm/danceability as tie-breakers.

- Add diversity + freshness: a secondary sort key or small randomization so the same profile doesn't get the identical list every run.

- Rebalance the catalog: add more songs in under-represented genres/moods and in the mid-energy gap (0.65–0.75) so niche and moderate-energy users get relevant matches

---

## 9. Personal Reflection  

- Through this project, I learned how recommender systems work and how they can be used to recommend music to users based on their preferences. 
- I also learned about the importance of balancing multiple factors when making recommendations, and how the model can sometimes recommend songs that are not in the user's preferred genre but have a similar mood or energy level. 
- I used AI to generate code and come up with the algorithm for the recommender system. It was not smart enough to think of the edge cases on its own and needed to be asked about it.
- 'Algorithm' to me is a big word, I'm glad AI made it simpler.
- I want to fulfill the future work section and make the model more robust and accurate. I also hope to combine collaborative filtering into this model.
