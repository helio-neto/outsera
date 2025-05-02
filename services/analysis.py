from typing import List, Tuple, Dict
from collections import defaultdict
import re


def analyze_movie_winners(raw_winner_list: List[Tuple[int, str]]) -> Dict[str, list]:
    """
    Analyzes the list of movie winners and it's producers and returns the producers with 
    the minimum and maximum intervals between wins.
    Handles multiple producers per movie.
    """
    producer_wins = defaultdict(list)
    # Group years by individual producer
    for year, producers_str in raw_winner_list:
        # Normalize delimiters: replace ' and ' (case-insensitive) with ','
        normalized = re.sub(r'\s+and\s+', ',', producers_str, flags=re.IGNORECASE)
        producers = [p.strip() for p in normalized.split(',') if p.strip()]
        for producer in producers:
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
