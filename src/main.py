"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 60)
    print("  TOP RECOMMENDATIONS")
    print(f"  For: genre={user_prefs['genre']}, "
          f"mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print("=" * 60)

    for rank, rec in enumerate(recommendations, start=1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"\n  {rank}.  {song['title']} - {song['artist']}")
        print(f"      Score: {score:.2f}  |  {song['genre']}, {song['mood']}")
        print(f"      Because: {explanation}")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
