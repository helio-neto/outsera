from typing import List, Tuple, Dict
from collections import defaultdict
import re


def analyze_movie_winners(raw_winner_list: List[Tuple[int, str]]) -> Dict[str, list]:
    """
    Analyzes movie winners to find producers with minimum and maximum intervals between wins.
    
    Args:
        raw_winner_list (List[Tuple[int, str]]): A list of tuples containing:
            - First element: Year of the win (int)
            - Second element: Producers' names (str), which can be comma or 'and' separated
    
    Returns:
        Dict[str, list]: A dictionary with two keys:
            - 'min': List of producers with the shortest interval between wins
            - 'max': List of producers with the longest interval between wins
    
    Each interval entry contains:
        - 'producer': Name of the producer
        - 'interval': Number of years between wins
        - 'previousWin': Year of the previous win
        - 'followingWin': Year of the following win
    
    Example:
        >>> winners = [(2000, 'John Smith'), (2003, 'John Smith, Jane Doe'), (2010, 'Jane Doe')]
        >>> result = analyze_movie_winners(winners)
        >>> # Possible output:
        >>> # {
        >>> #   'min': [{'producer': 'John Smith', 'interval': 3, 'previousWin': 2000, 'followingWin': 2003}],
        >>> #   'max': [{'producer': 'Jane Doe', 'interval': 7, 'previousWin': 2003, 'followingWin': 2010}]
        >>> # }
    """
    producer_wins = defaultdict(list)
    # Group years by individual producer
    for year, producers_str in raw_winner_list:
        # Normalize producers' names delimiters: replace ' and ' (case-insensitive) with ','
        normalized_list = re.sub(r'\s+and\s+', ',', producers_str, flags=re.IGNORECASE)
        producers = [producer.strip() for producer in normalized_list.split(',') if producer.strip()]
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
    # Populate min and max lists
    min_list = [producer for producer in intervals if producer['interval'] == min_interval]
    max_list = [producer for producer in intervals if producer['interval'] == max_interval]
    
    return {'min': min_list, 'max': max_list}
