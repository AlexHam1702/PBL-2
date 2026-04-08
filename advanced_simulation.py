"""
Advanced Auction Simulation - Multi-Round Strategy Analysis
Implements 500+ round simulations with multiple player strategies
"""

import random
import csv
import time
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
import matplotlib.pyplot as plt
import numpy as np

# --- ENHANCED BST WITH SUCCESSOR/PREDECESSOR ---

class Node:
    def __init__(self, price, player_name):
        self.price = price
        self.players = [player_name]
        self.left = None
        self.right = None
        self.parent = None  # Added for successor/predecessor

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
                node.left.parent = node
            else:
                self._insert_recursive(node.left, price, player_name)
        else:
            if node.right is None:
                node.right = Node(price, player_name)
                node.right.parent = node
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

    def find_successor(self, price):
        """Find the smallest price greater than the given price."""
        node = self._find_node(self.root, price)
        if node is None:
            return None

        # Case 1: Node has right subtree
        if node.right:
            return self._min_value(node.right)

        # Case 2: No right subtree, go up to find successor
        parent = node.parent
        while parent and node == parent.right:
            node = parent
            parent = parent.parent
        return parent.price if parent else None

    def find_predecessor(self, price):
        """Find the largest price smaller than the given price."""
        node = self._find_node(self.root, price)
        if node is None:
            return None

        # Case 1: Node has left subtree
        if node.left:
            return self._max_value(node.left)

        # Case 2: No left subtree, go up to find predecessor
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent
        return parent.price if parent else None

    def _find_node(self, node, price):
        """Find node with given price."""
        if node is None or node.price == price:
            return node
        if price < node.price:
            return self._find_node(node.left, price)
        return self._find_node(node.right, price)

    def _min_value(self, node):
        """Find minimum value in subtree."""
        current = node
        while current.left:
            current = current.left
        return current.price

    def _max_value(self, node):
        """Find maximum value in subtree."""
        current = node
        while current.right:
            current = current.right
        return current.price

    def clear(self):
        self.root = None
        self.all_bids = []

    def get_all_bids_sorted(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def get_height(self):
        """Calculate tree height for analysis."""
        return self._get_height(self.root)

    def _get_height(self, node):
        if node is None:
            return 0
        return 1 + max(self._get_height(node.left), self._get_height(node.right))

# --- PLAYER STRATEGIES ---

class PlayerStrategy:
    """Base class for bidding strategies."""

    def __init__(self, name: str, base_cost: float = 1.0, alpha: float = 100.0):
        self.name = name
        self.base_cost = base_cost
        self.alpha = alpha

    def calculate_cost(self, bid: int) -> float:
        """Calculate the cost of a bid."""
        return self.base_cost + (self.alpha / (bid + 1))

    def decide_bid(self, round_data: Dict) -> int:
        """Decide what bid to place. Override in subclasses."""
        raise NotImplementedError

class ConservativeStrategy(PlayerStrategy):
    """Conservative strategy: Always bid low, avoid duplicates."""

    def __init__(self, base_cost: float = 1.0, alpha: float = 100.0):
        super().__init__("Conservative", base_cost, alpha)
        self.previous_bids = set()

    def decide_bid(self, round_data: Dict) -> int:
        """Bid conservatively - choose low unique values."""
        existing_bids = round_data.get('existing_bids', set())
        min_bid = round_data.get('min_possible_bid', 0)
        max_bid = round_data.get('max_possible_bid', 100)

        # Try to find a low unique bid
        for bid in range(min_bid, max_bid + 1):
            if bid not in existing_bids:
                return bid

        # Fallback to random low bid
        return random.randint(min_bid, min(max_bid, 20))

class AggressiveStrategy(PlayerStrategy):
    """Aggressive strategy: Bid high to win, but risk duplicates."""

    def __init__(self, base_cost: float = 1.0, alpha: float = 100.0):
        super().__init__("Aggressive", base_cost, alpha)

    def decide_bid(self, round_data: Dict) -> int:
        """Bid aggressively - choose higher values."""
        existing_bids = round_data.get('existing_bids', set())
        min_bid = round_data.get('min_possible_bid', 0)
        max_bid = round_data.get('max_possible_bid', 100)

        # Prefer higher bids, but avoid obvious duplicates
        candidates = []
        for bid in range(max(min_bid, 50), max_bid + 1):
            if bid not in existing_bids:
                candidates.append(bid)

        if candidates:
            return random.choice(candidates[-5:])  # Choose from highest 5

        # Fallback
        return random.randint(max(min_bid, 30), max_bid)

class AdaptiveStrategy(PlayerStrategy):
    """Adaptive strategy: Learn from previous rounds and adjust."""

    def __init__(self, base_cost: float = 1.0, alpha: float = 100.0):
        super().__init__("Adaptive", base_cost, alpha)
        self.round_history = []
        self.successful_bids = []

    def decide_bid(self, round_data: Dict) -> int:
        """Adapt based on previous round outcomes."""
        existing_bids = round_data.get('existing_bids', set())
        min_bid = round_data.get('min_possible_bid', 0)
        max_bid = round_data.get('max_possible_bid', 100)

        # Learn from successful bids
        if self.successful_bids:
            avg_success = sum(self.successful_bids) / len(self.successful_bids)
            # Try similar bids
            target = int(avg_success + random.randint(-5, 5))
            target = max(min_bid, min(max_bid, target))
            if target not in existing_bids:
                return target

        # Default to moderate bid
        return random.randint(max(min_bid, 20), min(max_bid, 60))

    def record_result(self, bid: int, won: bool):
        """Record round result for learning."""
        if won:
            self.successful_bids.append(bid)
            # Keep only recent successful bids
            if len(self.successful_bids) > 10:
                self.successful_bids.pop(0)

class RandomStrategy(PlayerStrategy):
    """Random strategy: Bid randomly."""

    def __init__(self, base_cost: float = 1.0, alpha: float = 100.0):
        super().__init__("Random", base_cost, alpha)

    def decide_bid(self, round_data: Dict) -> int:
        """Bid completely randomly."""
        min_bid = round_data.get('min_possible_bid', 0)
        max_bid = round_data.get('max_possible_bid', 100)
        return random.randint(min_bid, max_bid)

# --- SIMULATION ENGINE ---

class AuctionSimulator:
    """Multi-round auction simulation engine."""

    def __init__(self, num_rounds: int = 500, players_per_round: int = 40):
        self.num_rounds = num_rounds
        self.players_per_round = players_per_round
        self.strategies = {}
        self.round_results = []
        self.player_stats = defaultdict(dict)

    def add_strategy(self, strategy_class, num_players: int, **kwargs):
        """Add a strategy with specified number of players."""
        strategy_name = kwargs.get('name', strategy_class.__name__)
        self.strategies[strategy_name] = {
            'class': strategy_class,
            'num_players': num_players,
            'kwargs': kwargs
        }

    def run_simulation(self, base_cost: float = 1.0, alpha: float = 100.0):
        """Run the multi-round simulation."""
        print(f"Starting {self.num_rounds}-round auction simulation...")
        print(f"Players per round: {self.players_per_round}")
        print(f"Strategies: {list(self.strategies.keys())}")
        print("-" * 60)

        start_time = time.time()

        for round_num in range(1, self.num_rounds + 1):
            if round_num % 50 == 0:
                print(f"Round {round_num}/{self.num_rounds}...")

            round_result = self._run_single_round(round_num, base_cost, alpha)
            self.round_results.append(round_result)

            # Update player statistics
            self._update_player_stats(round_result)

        end_time = time.time()
        print(".2f")
        print(f"Simulation completed: {len(self.round_results)} rounds")

    def _run_single_round(self, round_num: int, base_cost: float, alpha: float) -> Dict:
        """Run a single auction round."""
        bst = AuctionBST()
        players = []
        bids = []

        # Create players for this round
        player_id = 0
        for strategy_name, strategy_config in self.strategies.items():
            strategy_class = strategy_config['class']
            num_players = strategy_config['num_players']

            for i in range(num_players):
                player_id += 1
                player_name = f"{strategy_name[:3]}{player_id:02d}"

                # Create strategy instance
                kwargs = strategy_config['kwargs'].copy()
                kwargs['base_cost'] = base_cost
                kwargs['alpha'] = alpha
                strategy = strategy_class(**kwargs)

                players.append({
                    'name': player_name,
                    'strategy': strategy,
                    'strategy_name': strategy_name
                })

        # Each player places a bid
        existing_bids = set()
        for player in players:
            round_data = {
                'existing_bids': existing_bids.copy(),
                'min_possible_bid': 0,
                'max_possible_bid': 100,
                'round_num': round_num
            }

            bid = player['strategy'].decide_bid(round_data)
            bst.insert(bid, player['name'])
            bids.append((player['name'], bid))
            existing_bids.add(bid)

            # Record bid for adaptive strategies
            if hasattr(player['strategy'], 'record_result'):
                # We'll record results after winner is determined
                pass

        # Determine winner
        winning_price, winner = bst.find_lowest_unique()

        # Calculate seller revenue (sum of all bid costs)
        seller_revenue = 0
        for player_name, bid in bids:
            cost = base_cost + (alpha / (bid + 1))
            seller_revenue += cost

        # Record results for adaptive strategies
        for player in players:
            won = (player['name'] == winner)
            if hasattr(player['strategy'], 'record_result'):
                bid = next(b for name, b in bids if name == player['name'])
                player['strategy'].record_result(bid, won)

        round_result = {
            'round_num': round_num,
            'bids': bids,
            'winner': winner,
            'winning_price': winning_price,
            'seller_revenue': seller_revenue,
            'bst_height': bst.get_height(),
            'total_unique_prices': len(bst.get_all_bids_sorted()),
            'base_cost': base_cost,
            'alpha': alpha
        }

        return round_result

    def _update_player_stats(self, round_result: Dict):
        """Update player statistics."""
        winner = round_result['winner']
        winning_price = round_result['winning_price']

        # Group bids by strategy
        strategy_bids = defaultdict(list)
        for player_name, bid in round_result['bids']:
            strategy_name = None
            for s_name in self.strategies.keys():
                if player_name.startswith(s_name[:3]):
                    strategy_name = s_name
                    break
            if strategy_name:
                strategy_bids[strategy_name].append((player_name, bid))

        # Update stats for each strategy
        for strategy_name, bids in strategy_bids.items():
            if strategy_name not in self.player_stats:
                self.player_stats[strategy_name] = {
                    'rounds_played': 0,
                    'wins': 0,
                    'total_profit': 0,
                    'total_cost': 0,
                    'avg_bid': 0,
                    'win_rate': 0
                }

            stats = self.player_stats[strategy_name]
            stats['rounds_played'] += 1

            # Check if this strategy won
            if winner and any(name == winner for name, _ in bids):
                stats['wins'] += 1

            # Calculate costs and profits
            round_cost = 0
            round_profit = 0
            total_bid = 0

            for player_name, bid in bids:
                cost = round_result['base_cost'] + (round_result['alpha'] / (bid + 1))
                round_cost += cost
                total_bid += bid

                # Profit calculation: if won, profit = winning_price - cost
                # if lost, profit = -cost
                if player_name == winner and winner:
                    profit = winning_price - cost
                else:
                    profit = -cost

                round_profit += profit

            stats['total_cost'] += round_cost
            stats['total_profit'] += round_profit
            stats['avg_bid'] = (stats['avg_bid'] * (stats['rounds_played'] - 1) + total_bid / len(bids)) / stats['rounds_played']
            stats['win_rate'] = stats['wins'] / stats['rounds_played']

    def get_strategy_comparison(self) -> Dict:
        """Get comprehensive strategy comparison."""
        comparison = {}

        for strategy_name, stats in self.player_stats.items():
            rounds = stats['rounds_played']
            comparison[strategy_name] = {
                'win_rate': stats['win_rate'] * 100,
                'avg_profit_per_round': stats['total_profit'] / rounds if rounds > 0 else 0,
                'avg_cost_per_round': stats['total_cost'] / rounds if rounds > 0 else 0,
                'avg_bid': stats['avg_bid'],
                'total_rounds': rounds,
                'total_wins': stats['wins']
            }

        # Overall seller revenue stats
        seller_revenues = [r['seller_revenue'] for r in self.round_results]
        comparison['seller_stats'] = {
            'avg_revenue_per_round': sum(seller_revenues) / len(seller_revenues),
            'total_revenue': sum(seller_revenues),
            'min_revenue': min(seller_revenues),
            'max_revenue': max(seller_revenues)
        }

        return comparison

    def analyze_bst_performance(self) -> Dict:
        """Analyze BST performance across rounds."""
        heights = [r['bst_height'] for r in self.round_results]
        unique_prices = [r['total_unique_prices'] for r in self.round_results]

        return {
            'avg_tree_height': sum(heights) / len(heights),
            'max_tree_height': max(heights),
            'avg_unique_prices': sum(unique_prices) / len(unique_prices),
            'height_distribution': Counter(heights)
        }

    def run_parameter_sensitivity(self, base_costs: List[float], alphas: List[float]) -> Dict:
        """Test different parameter combinations."""
        results = {}

        for base_cost in base_costs:
            for alpha in alphas:
                print(f"Testing base_cost={base_cost}, alpha={alpha}")

                # Quick simulation with fewer rounds
                mini_sim = AuctionSimulator(num_rounds=50, players_per_round=self.players_per_round)
                for strategy_name, config in self.strategies.items():
                    mini_sim.add_strategy(config['class'], config['num_players'], **config['kwargs'])

                mini_sim.run_simulation(base_cost, alpha)
                comparison = mini_sim.get_strategy_comparison()

                key = f"bc{base_cost}_a{alpha}"
                results[key] = {
                    'base_cost': base_cost,
                    'alpha': alpha,
                    'strategies': comparison
                }

        return results

# --- ALTERNATIVE IMPLEMENTATIONS ---

class DictionaryAuction:
    """Alternative implementation using dictionary + sort."""

    def __init__(self):
        self.bids = defaultdict(list)

    def insert(self, price, player_name):
        self.bids[price].append(player_name)

    def find_lowest_unique(self):
        # Sort prices and find lowest unique
        sorted_prices = sorted(self.bids.keys())
        for price in sorted_prices:
            if len(self.bids[price]) == 1:
                return price, self.bids[price][0]
        return None, None

    def clear(self):
        self.bids.clear()

class HeapAuction:
    """Alternative implementation using heap."""

    def __init__(self):
        import heapq
        self.bids = []
        self.bid_counts = defaultdict(int)

    def insert(self, price, player_name):
        import heapq
        heapq.heappush(self.bids, (price, player_name))
        self.bid_counts[price] += 1

    def find_lowest_unique(self):
        # Find lowest price with count == 1
        for price, count in sorted(self.bid_counts.items()):
            if count == 1:
                # Find the player with this price
                for bid_price, player in self.bids:
                    if bid_price == price:
                        return price, player
        return None, None

    def clear(self):
        self.bids.clear()
        self.bid_counts.clear()

# --- PERFORMANCE COMPARISON ---

def benchmark_implementations(num_rounds=100, players_per_round=40):
    """Benchmark different auction implementations."""
    implementations = {
        'BST': AuctionBST,
        'Dictionary': DictionaryAuction,
        'Heap': HeapAuction
    }

    results = {}

    for name, impl_class in implementations.items():
        print(f"Benchmarking {name}...")

        start_time = time.time()
        total_winners = 0

        for round_num in range(num_rounds):
            auction = impl_class()

            # Generate random bids
            for i in range(players_per_round):
                bid = random.randint(0, 100)
                player = f"P{i:02d}"
                auction.insert(bid, player)

            winner_price, winner = auction.find_lowest_unique()
            if winner:
                total_winners += 1

        end_time = time.time()

        results[name] = {
            'time': end_time - start_time,
            'avg_time_per_round': (end_time - start_time) / num_rounds,
            'winners_found': total_winners
        }

    return results

# --- MAIN ANALYSIS ---

def run_comprehensive_analysis():
    """Run comprehensive strategy analysis."""
    print("=" * 80)
    print("COMPREHENSIVE AUCTION STRATEGY ANALYSIS")
    print("=" * 80)

    # Create simulator
    sim = AuctionSimulator(num_rounds=500, players_per_round=40)

    # Add strategies
    sim.add_strategy(ConservativeStrategy, 15)
    sim.add_strategy(AggressiveStrategy, 15)
    sim.add_strategy(AdaptiveStrategy, 8)
    sim.add_strategy(RandomStrategy, 2)

    # Run main simulation
    sim.run_simulation(base_cost=1.0, alpha=100.0)

    # Get results
    comparison = sim.get_strategy_comparison()
    bst_analysis = sim.analyze_bst_performance()

    # Print strategy comparison
    print("\n" + "=" * 60)
    print("STRATEGY COMPARISON RESULTS")
    print("=" * 60)

    print(f"{'Strategy':<12} {'Win Rate':<10} {'Avg Profit':<12} {'Avg Cost':<10} {'Avg Bid':<10}")
    print("-" * 60)

    for strategy, stats in comparison.items():
        if strategy != 'seller_stats':
            print(f"{strategy:<12} {stats['win_rate']:<10.1f} {stats['avg_profit_per_round']:<12.2f} {stats['avg_cost_per_round']:<10.2f} {stats['avg_bid']:<10.1f}")

    # Seller stats
    seller = comparison['seller_stats']
    print("\nSELLER REVENUE STATISTICS:")
    print(f"Average Revenue per Round: {seller['avg_revenue_per_round']:.2f}")
    print(f"Total Revenue: {seller['total_revenue']:.2f}")
    print(f"Min Revenue: {seller['min_revenue']:.2f}")
    print(f"Max Revenue: {seller['max_revenue']:.2f}")

    # BST Analysis
    print("\nBST PERFORMANCE ANALYSIS:")
    print(f"Average Tree Height: {bst_analysis['avg_tree_height']:.2f}")
    print(f"Max Tree Height: {bst_analysis['max_tree_height']}")
    print(f"Average Unique Prices: {bst_analysis['avg_unique_prices']:.2f}")

    # Parameter sensitivity
    print("\nPARAMETER SENSITIVITY ANALYSIS:")
    print("Testing different base_cost and alpha values...")

    base_costs = [0.5, 1.0, 2.0]
    alphas = [50.0, 100.0, 200.0]

    param_results = sim.run_parameter_sensitivity(base_costs, alphas)

    print("\nParameter Effects on Win Rates:")
    print(f"{'Parameters':<15} {'Conservative':<12} {'Aggressive':<12} {'Adaptive':<12} {'Random':<12}")
    print("-" * 60)

    for param_key, data in param_results.items():
        bc = data['base_cost']
        a = data['alpha']
        strategies = data['strategies']

        print(f"bc{bc}_a{a:<11}")
        for s_name in ['Conservative', 'Aggressive', 'Adaptive', 'Random']:
            if s_name in strategies:
                win_rate = strategies[s_name]['win_rate']
                print(f"{win_rate:<12.1f}", end="")
        print()

    # Benchmark implementations
    print("\nIMPLEMENTATION PERFORMANCE COMPARISON:")
    print("Benchmarking BST vs Dictionary vs Heap implementations...")

    benchmarks = benchmark_implementations(num_rounds=100, players_per_round=40)

    print(f"{'Implementation':<12} {'Time (s)':<10} {'Avg/round (ms)':<15} {'Winners':<8}")
    print("-" * 50)

    for impl, stats in benchmarks.items():
        print(f"{impl:<12} {stats['time']:<10.3f} {stats['avg_time_per_round']*1000:<15.2f} {stats['winners_found']:<8}")

    # BST Successor/Predecessor Analysis
    print("\nBST SUCCESSOR/PREDECESSOR ANALYSIS:")
    print("Demonstrating successor and predecessor operations...")

    demo_bst = AuctionBST()
    demo_bids = [25, 15, 35, 10, 20, 30, 40, 5, 12, 18, 22, 28, 32, 38, 45]

    for bid in demo_bids:
        demo_bst.insert(bid, f"P{bid}")

    print("\nDemo BST with bids:", sorted(demo_bids))
    print("Testing successor/predecessor for various prices:")

    test_prices = [15, 20, 25, 30, 35]
    for price in test_prices:
        succ = demo_bst.find_successor(price)
        pred = demo_bst.find_predecessor(price)
        print(f"Price {price}: Successor={succ}, Predecessor={pred}")

    print("\nWhy successor/predecessor matter:")
    print("1. SUCCESSOR: Find next candidate after non-unique price")
    print("   - If price 20 is taken, successor 22 might be next option")
    print("   - Helps strategies find alternative bids efficiently")
    print("2. PREDECESSOR: Navigate backwards in price order")
    print("   - Useful for finding lower price alternatives")
    print("   - Helps in price range analysis")

    # BST Limitations Discussion
    print("\nBST LIMITATIONS & ALTERNATIVES:")
    print("1. DEGENERATION: Can become unbalanced (O(n) worst case)")
    print("   - Solution: Self-balancing trees (AVL, Red-Black)")
    print("2. MEMORY: Each node stores parent pointers")
    print("   - Alternative: Dictionary + sort (simpler, O(n log n))")
    print("3. COMPLEXITY: More complex than simple data structures")
    print("   - Alternative: Heap (O(n) build, O(log n) insert)")

    print("\nPerformance Impact:")
    print("- BST: O(log n) insert, O(n) find winner")
    print("- Dictionary+Sort: O(n) insert, O(n log n) find winner")
    print("- Heap: O(log n) insert, O(n) find winner")
    print("- BST wins for frequent inserts, Dictionary for simple cases")

    return sim, comparison, benchmarks

if __name__ == '__main__':
    # Run comprehensive analysis
    simulator, results, benchmarks = run_comprehensive_analysis()

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("Check the results above for detailed strategy comparisons!")
    print("=" * 80)