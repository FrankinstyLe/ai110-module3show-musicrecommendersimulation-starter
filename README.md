# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

My recommender is a **content-based** system: it recommends songs that *sound and feel like* what the user says they want. It works in two clear steps — **score every song**, then **rank and trim** the list.

### What features does each `Song` use?

Each `Song` stores ten fields, but only four actually drive the recommendation:

- **`genre`** (e.g. pop, lofi, rock) — the style of the song.
- **`mood`** (e.g. happy, chill, intense) — the feeling it gives off.
- **`energy`** (0–1) — how intense or laid-back it is.
- **`acousticness`** (0–1) — how acoustic vs. electronic it sounds.

The song also carries `id`, `title`, and `artist` (labels for display, not scoring) and `tempo_bpm`, `valence`, and `danceability` (extra audio features I keep on hand for future experiments but don't score on yet).

### What does the `UserProfile` store?

A user's "taste profile" is four preferences:

- **`favorite_genre`** — the genre they're in the mood for.
- **`favorite_mood`** — the vibe they want.
- **`target_energy`** (0–1) — how energetic they want the music.
- **`likes_acoustic`** (True/False) — whether they prefer acoustic tracks.

### How does the `Recommender` compute a score for each song?

For one song, it adds up four rewards (all handled in `_score_song_attrs`):

| What's checked | How it's scored | Points |
|---|---|---|
| Genre matches favorite | exact match | **+2.0** |
| Mood matches favorite | exact match | **+1.5** |
| Energy close to target | `1 − abs(target − energy)`, then ×2.0 | **up to +2.0** |
| Acoustic preference | rewards acoustic if `likes_acoustic`, else non-acoustic | **up to +1.0** |

The closer a song is to the profile, the higher its total. Along the way the scorer also collects plain-English **reasons** (e.g. *"matches your favorite genre (pop)"*) so the recommendation can explain itself.

### How do I choose which songs to recommend?

1. **Score** every song in the catalog with the rule above.
2. **Sort** them from highest score to lowest.
3. **Keep the top `k`** (default 5) and hand them back with their explanations.

So the final list is simply *"the k songs that best match this profile, best first."*

```
UserProfile ─┐
             ├─►  score each Song  ─►  sort high→low  ─►  keep top k  ─►  recommendations
  all Songs ─┘        (Scoring Rule)      (Ranking Rule)
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
============================================================
  TOP RECOMMENDATIONS
  For: genre=pop, mood=happy, energy=0.8
============================================================

  1.  Sunrise City - Neon Echo
      Score: 6.28  |  pop, happy
      Because: matches your favorite genre (pop), matches your mood (happy), energy level is a great fit, energetic, non-acoustic sound

  2.  Gym Hero - Max Pulse
      Score: 4.69  |  pop, intense
      Because: matches your favorite genre (pop), energy level is a great fit, energetic, non-acoustic sound

  3.  Rooftop Lights - Indigo Parade
      Score: 4.07  |  indie pop, happy
      Because: matches your mood (happy), energy level is a great fit

  4.  Concrete Kingdom - Blocktext
      Score: 2.88  |  hip hop, confident
      Because: energy level is a great fit, energetic, non-acoustic sound

  5.  Late Shift Funk - The Groove Unit
      Score: 2.76  |  funk, playful
      Because: energy level is a great fit, energetic, non-acoustic sound

============================================================
```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



