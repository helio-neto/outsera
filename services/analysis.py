from typing import List, Tuple, Dict
from collections import defaultdict


def analysis_movie_winners(raw_winner_list: List[Tuple[int, str]]) -> Dict[str, list]:
    """
    Given a list of (year, producer) tuples, returns a dict with 'min' and 'max' time
    that a producer has won the Golden Raspberry Awards.
    """
    producer_wins = defaultdict(list)
    # Group years by producer
    for year, producer in raw_winner_list:
        producer_wins[producer].append(year)

    intervals = []  # List of (producer, interval, previousWin, followingWin)
    for producer, years in producer_wins.items():
        years = sorted(years)
        for i in range(1, len(years)):
            interval = years[i] - years[i-1]
            intervals.append({
                'producer': producer,
                'interval': interval,
                'previousWin': years[i-1],
                'followingWin': years[i]
            })

    if not intervals:
        return {'min': [], 'max': []}

    # Find min and max interval values
    min_interval = min(intervals, key=lambda x: x['interval'])['interval']
    max_interval = max(intervals, key=lambda x: x['interval'])['interval']

    min_list = [d for d in intervals if d['interval'] == min_interval]
    max_list = [d for d in intervals if d['interval'] == max_interval]

    return {'min': min_list, 'max': max_list}
