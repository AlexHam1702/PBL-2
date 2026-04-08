# Auction Simulator - Usage Guide

## Overview
The auction simulation code has been updated to automatically load and simulate auction rounds from the CSV files in the `bid_data/` folder. The system uses a Binary Search Tree (BST) to efficiently find the winner of each auction using the "Lowest Unique Bid" algorithm.

## Files

### Core Application Files
- **main.py**: PyQt5 GUI application with two modes:
  - Manual bid entry (interactive)
  - Automated auction simulation from CSV files
  
- **auction_simulator.py**: Command-line batch simulation tool for analyzing multiple auction files

### Bid Data Files
Located in `bid_data/` folder:
- **lowbid_manche_demo.csv**: Demo auction with 30 participants, single round
- **lowbid_multi_manches_500x40.csv**: Multi-round auction with 500 rounds, 40 players each
- **lowbid_stress_200k.csv**: Large-scale stress test auction with 200,000+ bids

## How to Use

### 1. GUI Application (main.py)
Run the PyQt5 GUI application:
```bash
python main.py
```

**Features:**
- **File Selection**: Use the dropdown menu to select a bid data file from the `bid_data/` folder
- **Load & Simulate**: Click "Load & Simulate" to analyze the selected file
- **Manual Entry**: Enter player names and bid amounts manually
- **Calculate Winner**: Find the winner based on the "Lowest Unique Bid" rule
- **Clear All**: Reset the auction data

**Display Output:**
- Total participants and unique prices
- Winner name and winning bid amount
- Price statistics (min, max, average)
- Complete bid listing showing which bids are unique vs duplicated

### 2. Command-Line Simulator (auction_simulator.py)
Run all auction simulations:
```bash
python auction_simulator.py
```

Simulate a specific file:
```bash
python auction_simulator.py lowbid_manche_demo.csv
```

**Features:**
- Automatically detects multi-round auctions (files with "manche" column)
- Provides comprehensive statistics for each auction
- Shows summary of all auction results
- Supports stress-testing with large datasets

## Algorithm: Lowest Unique Bid

**Rules:**
1. All player bids are inserted into a Binary Search Tree
2. The tree is traversed in-order (sorted by price)
3. The winner is the player with the lowest bid that is unique (no other player bid the same amount)

**Example:**
- Bids: J01=5€, J02=3€, J03=3€, J04=7€
- Unique bids: 5€ (J01), 7€ (J04)
- Lowest unique bid: 5€
- **Winner: J01**

## Data Format

### Single Round Format (lowbid_manche_demo.csv)
```
joueur,prix
J01,2
J02,30
J03,3
```

### Multi-Round Format (lowbid_multi_manches_500x40.csv)
```
manche,joueur,prix
1,J01,42
1,J02,54
2,J01,35
2,J02,48
```

## Output Examples

### Single Round Simulation
```
======================================================================
AUCTION SIMULATION: lowbid_manche_demo.csv
======================================================================

Total Participants: 30
Total Unique Prices: 23

[WINNER] J13
   Winning Bid: 0€

Price Statistics:
  - Minimum: 0€
  - Maximum: 49€
  - Average: 26.20€
```

### Multi-Round Simulation
```
======================================================================
MULTI-ROUND AUCTION: lowbid_multi_manches_500x40.csv (500 rounds)
======================================================================

Round Winners Summary:
----------------------------------------------------------------------
Round      Winner                         Price
----------------------------------------------------------------------
1          J14                            1
2          J06                            N/A
3          J19                            1
...
```

## Features

### BST (Binary Search Tree) Implementation
The code uses a custom BST data structure to:
- Store bids efficiently in O(log n) average time
- Handle duplicate bids (multiple players with same bid)
- Traverse and find the lowest unique bid in O(n) time

### Statistics Provided
- **Total Participants**: Number of players in the auction
- **Total Unique Prices**: Number of distinct bid amounts
- **Price Statistics**: Minimum, maximum, and average bids
- **Bid Analysis**: Shows all prices, player counts, and uniqueness

### Multi-Round Support
For files containing multiple auction rounds (manche):
- Each round is analyzed separately
- Winners and prices are displayed for each round
- Summary table shows all round results

## Technical Details

### Time Complexity
- **Insert Operation**: O(log n) average, O(n) worst case
- **Find Lowest Unique**: O(n)
- **Overall Simulation**: O(n log n)

### Space Complexity
- O(n) for storing all bids in the BST

## Troubleshooting

### Issue: File not found
- Ensure CSV files are in the `bid_data/` folder
- Check filename spelling matches exactly

### Issue: Invalid bid prices
- Ensure all bid prices are valid integers
- Non-integer prices are automatically skipped with warning

### Issue: No unique winner found
- All bids are duplicated with no unique amounts
- Example: All players bid the same amount

## Future Enhancements

Possible improvements:
- Export results to CSV files
- Visualize auction data with charts
- Add more auction algorithms (sealed-bid, ascending price, etc.)
- Support for weighted bids
- Real-time auction simulation
- Performance benchmarking framework
