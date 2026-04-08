"""
Auction Simulator - Command-line script for batch auction simulations
Loads bid data from CSV files and analyzes auction rounds
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

# --- BST IMPLEMENTATION ---

class Node:
    def __init__(self, price, player_name):
        self.price = price
        self.players = [player_name]
        self.left = None
        self.right = None

class AuctionBST:
    def __init__(self):
        self.root = None
        self.all_bids = []

    def insert(self, price, player_name):
        self.all_bids.append((price, player_name))
        if not self.root:
            self.root = Node(price, player_name)
        else:
            self._insert_recursive(self.root, price, player_name)

    def _insert_recursive(self, node, price, player_name):
        if price == node.price:
            node.players.append(player_name)
        elif price < node.price:
            if node.left is None:
                node.left = Node(price, player_name)
            else:
                self._insert_recursive(node.left, price, player_name)
        else:
            if node.right is None:
                node.right = Node(price, player_name)
            else:
                self._insert_recursive(node.right, price, player_name)

    def find_lowest_unique(self):
        """Find the lowest unique bid."""
        uniques = []
        self._inorder_traversal(self.root, uniques)
        for price, players in uniques:
            if len(players) == 1:
                return price, players[0]
        return None, None

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append((node.price, node.players))
            self._inorder_traversal(node.right, result)

    def clear(self):
        self.root = None
        self.all_bids = []

    def get_all_bids_sorted(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result


# --- SIMULATION FUNCTIONS ---

def load_bids_with_manches(filepath):
    """Load bids from CSV file and organize by manche (round) if present."""
    try:
        rounds_data = defaultdict(list)
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            has_manche = 'manche' in fieldnames
            
            for row in reader:
                player_name = row['joueur'].strip()
                try:
                    price = int(row['prix'].strip())
                    
                    if has_manche:
                        manche = int(row['manche'].strip())
                        rounds_data[manche].append((player_name, price))
                    else:
                        # Single round - use key 1
                        rounds_data[1].append((player_name, price))
                except (ValueError, TypeError, KeyError):
                    # Skip invalid rows
                    continue
        
        # Return sorted by round number
        return dict(sorted(rounds_data.items()))
    except Exception as e:
        print(f"Error loading file {filepath}: {str(e)}")
        return {}


def simulate_auction(filename, bids):
    """Run auction simulation on loaded bids."""
    bst = AuctionBST()
    
    # Insert all bids
    for player_name, price in bids:
        bst.insert(price, player_name)
    
    # Find winner
    winning_price, winner = bst.find_lowest_unique()
    
    # Get statistics
    sorted_bids = bst.get_all_bids_sorted()
    prices = [b[1] for b in bids]  # b[1] is the price, b[0] is player_name
    
    results = {
        'filename': filename,
        'total_participants': len(bids),
        'total_unique_prices': len(sorted_bids),
        'winner': winner,
        'winning_price': winning_price,
        'min_price': min(prices),
        'max_price': max(prices),
        'avg_price': sum(prices) / len(prices),
        'sorted_bids': sorted_bids,
        'all_bids': bids
    }
    
    return results


def print_results(results):
    """Print formatted auction results."""
    print(f"\n{'='*70}")
    print(f"AUCTION SIMULATION: {results['filename']}")
    print(f"{'='*70}\n")
    
    print(f"Total Participants: {results['total_participants']}")
    print(f"Total Unique Prices: {results['total_unique_prices']}\n")
    
    # Winner info
    if results['winner']:
        print(f"[WINNER] {results['winner']}")
        print(f"   Winning Bid: {results['winning_price']}€\n")
    else:
        print(f"[NO UNIQUE WINNER] - All bids are duplicated\n")
    
    # Statistics
    print(f"Price Statistics:")
    print(f"  - Minimum: {results['min_price']}€")
    print(f"  - Maximum: {results['max_price']}€")
    print(f"  - Average: {results['avg_price']:.2f}€\n")
    
    # Bid distribution
    print(f"Bid Analysis:")
    print(f"{'-'*70}")
    print(f"{'Price':<10} {'Count':<8} {'Players':<50} {'Unique?':<5}")
    print(f"{'-'*70}")
    
    for price, players in results['sorted_bids']:
        is_unique = "YES" if len(players) == 1 else "NO"
        player_str = ", ".join(players[:4])
        if len(players) > 4:
            player_str += f"... (+{len(players)-4})"
        print(f"{price:<10} {len(players):<8} {player_str:<50} {is_unique:<5}")
    
    print(f"{'-'*70}\n")


def find_bid_files():
    """Find all CSV files in bid_data folder."""
    bid_data_path = Path(__file__).parent / "bid_data"
    if bid_data_path.exists():
        return sorted(list(bid_data_path.glob("*.csv")))
    return []


def simulate_all():
    """Simulate all available auction files."""
    bid_files = find_bid_files()
    
    if not bid_files:
        print("No bid data files found in bid_data folder.")
        return
    
    print(f"\nFound {len(bid_files)} bid data file(s):")
    for i, f in enumerate(bid_files, 1):
        print(f"  {i}. {f.name}")
    
    all_results = []
    for bid_file in bid_files:
        rounds_data = load_bids_with_manches(bid_file)
        if rounds_data:
            if len(rounds_data) > 1:
                # Multiple rounds - show summary
                print(f"\n{'='*70}")
                print(f"MULTI-ROUND AUCTION: {bid_file.name} ({len(rounds_data)} rounds)")
                print(f"{'='*70}\n")
                
                round_winners = []
                for round_num in sorted(rounds_data.keys()):
                    bids = rounds_data[round_num]
                    results = simulate_auction(f"{bid_file.name} - Round {round_num}", bids)
                    round_winners.append((round_num, results['winner'], results['winning_price']))
                    all_results.append(results)
                
                # Show winner summary for all rounds
                print(f"\nRound Winners Summary:")
                print(f"{'-'*70}")
                print(f"{'Round':<10} {'Winner':<30} {'Price':<10}")
                print(f"{'-'*70}")
                for round_num, winner, price in round_winners:
                    winner_str = winner if winner else "None"
                    price_str = str(price) if price else "N/A"
                    print(f"{round_num:<10} {winner_str:<30} {price_str:<10}")
                print(f"{'-'*70}\n")
            else:
                # Single round
                bids = list(rounds_data.values())[0]
                results = simulate_auction(bid_file.name, bids)
                all_results.append(results)
                print_results(results)
    
    # Summary
    if all_results:
        print(f"\n{'='*70}")
        print(f"SUMMARY OF ALL AUCTIONS")
        print(f"{'='*70}\n")
        print(f"{'File':<45} {'Winner':<20} {'Price':<10}")
        print(f"{'-'*75}")
        for r in all_results:
            winner = r['winner'] if r['winner'] else "None"
            price = str(r['winning_price']) if r['winning_price'] else "N/A"
            print(f"{r['filename']:<45} {winner:<20} {price:<10}")
        print(f"{'-'*75}\n")


def simulate_single(filename):
    """Simulate a specific auction file."""
    bid_data_path = Path(__file__).parent / "bid_data" / filename
    
    if not bid_data_path.exists():
        print(f"File not found: {bid_data_path}")
        return
    
    rounds_data = load_bids_with_manches(bid_data_path)
    if rounds_data:
        if len(rounds_data) > 1:
            print(f"\n{'='*70}")
            print(f"MULTI-ROUND AUCTION: {filename} ({len(rounds_data)} rounds)")
            print(f"{'='*70}\n")
            
            round_winners = []
            for round_num in sorted(rounds_data.keys()):
                bids = rounds_data[round_num]
                results = simulate_auction(f"{filename} - Round {round_num}", bids)
                round_winners.append((round_num, results['winner'], results['winning_price']))
            
            # Show winner summary
            print(f"\nRound Winners Summary:")
            print(f"{'-'*70}")
            print(f"{'Round':<10} {'Winner':<30} {'Price':<10}")
            print(f"{'-'*70}")
            for round_num, winner, price in round_winners:
                winner_str = winner if winner else "None"
                price_str = str(price) if price else "N/A"
                print(f"{round_num:<10} {winner_str:<30} {price_str:<10}")
            print(f"{'-'*70}\n")
        else:
            # Single round
            bids = list(rounds_data.values())[0]
            results = simulate_auction(filename, bids)
            print_results(results)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Simulate specific file
        simulate_single(sys.argv[1])
    else:
        # Simulate all files
        simulate_all()
