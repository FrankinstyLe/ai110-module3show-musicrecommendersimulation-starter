import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Scoring weights (shared by both the OOP and functional implementations).
# These encode the "Algorithm Recipe": reward genre/mood matches, reward
# songs whose energy is close to what the user wants, and factor in whether
# the user likes acoustic tracks.
# ---------------------------------------------------------------------------
GENRE_MATCH_BONUS = 2.0
MOOD_MATCH_BONUS = 1.5
ENERGY_WEIGHT = 2.0
ACOUSTIC_WEIGHT = 1.0


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_song_attrs(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    likes_acoustic: bool,
) -> Tuple[float, List[str]]:
    """
    Core scoring routine used by both the OOP and functional interfaces.
    Returns (score, reasons) so callers can rank songs and explain why.
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if favorite_genre and genre == favorite_genre:
        score += GENRE_MATCH_BONUS
        reasons.append(f"matches your favorite genre ({genre})")

    # Mood match
    if favorite_mood and mood == favorite_mood:
        score += MOOD_MATCH_BONUS
        reasons.append(f"matches your mood ({mood})")

    # Energy closeness: closer to target -> higher score (max ENERGY_WEIGHT)
    if target_energy is not None:
        energy_closeness = 1.0 - abs(target_energy - energy)
        score += ENERGY_WEIGHT * energy_closeness
        if energy_closeness >= 0.8:
            reasons.append("energy level is a great fit")
        elif energy_closeness >= 0.5:
            reasons.append("energy level is a decent fit")

    # Acoustic preference
    if likes_acoustic:
        score += ACOUSTIC_WEIGHT * acousticness
        if acousticness >= 0.6:
            reasons.append("nice and acoustic, like you prefer")
    else:
        # Reward non-acoustic tracks slightly when the user doesn't want acoustic
        score += ACOUSTIC_WEIGHT * (1.0 - acousticness)
        if acousticness <= 0.3:
            reasons.append("energetic, non-acoustic sound")

    if not reasons:
        reasons.append("a reasonable all-round match")

    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        return _score_song_attrs(
            genre=song.genre,
            mood=song.mood,
            energy=song.energy,
            acousticness=song.acousticness,
            favorite_genre=user.favorite_genre,
            favorite_mood=user.favorite_mood,
            target_energy=user.target_energy,
            likes_acoustic=user.likes_acoustic,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda song: self._score(user, song)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score(user, song)
        return f"'{song.title}' recommended because it " + ", ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dicts with numeric fields
    converted to the correct types.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song (dict) against user preferences (dict).
    Required by recommend_songs() and src/main.py
    Expected return format: (score, reasons)
    """
    return _score_song_attrs(
        genre=song.get("genre", ""),
        mood=song.get("mood", ""),
        energy=song.get("energy", 0.0),
        acousticness=song.get("acousticness", 0.0),
        favorite_genre=user_prefs.get("genre", ""),
        favorite_mood=user_prefs.get("mood", ""),
        target_energy=user_prefs.get("energy"),
        likes_acoustic=user_prefs.get("likes_acoustic", False),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores and ranks all songs, returning the top k.
    Required by src/main.py
    Expected return format: (song_dict, score, explanation)
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
