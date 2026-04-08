# LIVE AUCTION - Real-Time Interactive Auction Simulator

## Overview
The enhanced auction application now features a **real-time live auction experience** where simulated bids appear one by one, and you can compete against them by placing your own bids in real-time!

## Key Features

### 1. **Live Bid Streaming**
- Bids appear one at a time with smooth animation
- Watch as each player places their bid in sequence
- See the current leader change as new bids arrive
- Numbered bid counter showing progress

### 2. **Adjustable Auction Speed**
- Speed slider controls how fast bids appear (100ms - 2000ms per bid)
- Pause and resume at any time to think strategically
- Find the perfect pace for your playstyle

### 3. **Real-Time Winner Updates**
- Current leader is displayed prominently with gold background
- Winner changes automatically as new bids come in
- Shows winning bid amount
- Displays if no unique winner exists yet

### 4. **Dynamic Statistics Panel**
- Minimum, maximum, and average bid amounts
- Lists lowest unique bids as they develop
- Updates in real-time as auction progresses
- Track price trends throughout the auction

### 5. **Interactive Player Bidding**
- Place your own bids during the auction
- Compete directly against simulated players
- See all your bids tracked in real-time
- Your bids affect the winner calculation immediately
- Cost calculation for each bid shown (based on algorithm formula)

## How to Play

### Starting a Live Auction

1. **Select Auction File**
   - Choose from dropdown: `lowbid_manche_demo.csv` (demo), `lowbid_multi_manches_500x40.csv` (multi-round), etc.

2. **Click START AUCTION**
   - Bids will begin appearing one by one
   - Live bid feed updates in real-time
   - Winner display shows current leader

### Bidding During the Auction

1. **Enter Your Name**
   - Type your player name in the "Your Player Name" field
   - This is your identity in the auction

2. **Place Your Bid**
   - Enter your bid amount in the "Your Bid Amount" field
   - Click "PLACE BID"
   - Your bid is immediately added to the auction
   - You compete directly against the simulated bids!

3. **Track Your Performance**
   - All your bids are listed in "YOUR BIDS" section
   - Includes bid amount and calculated cost
   - See if you're currently winning

### Controlling the Auction

**START AUCTION**
- Loads the selected bid file
- Begins streaming bids one at a time
- Button becomes disabled during auction

**PAUSE / RESUME**
- Pause to review statistics or place a strategic bid
- Click again to resume the auction
- Button label changes between PAUSE/RESUME

**RESET**
- Stop current auction and return to initial state
- Clear all bids from display
- Ready to select a new file and start over

**Speed Slider**
- Adjust bid display speed with slider (100-2000ms)
- Changes take effect immediately
- Faster = more intense, Slower = more thinking time

## Layout

### Left Panel - Live Bid Feed
```
[  1] J01     ->  42€
[  2] J02     ->  54€
[  3] J03     ->  47€
...
```
Shows each bid as it's added with sequential numbering.

### Center Panel - Current Winner & Statistics
**Upper Section:**
- Large, highlighted display of current winning player
- Shows bid amount
- Gold background for current leader
- Orange if no unique winner yet

**Statistics Section:**
- Price min/max/average
- Lowest unique bids list
- Progress counter (e.g., "50/100 bids shown")

### Right Panel - Your Bidding Area
**Input Fields:**
- Your Player Name
- Your Bid Amount

**PLACE BID Button**
- Adds your bid to the active auction
- Your bid competes with all other bids

**Your Bids Display:**
- History of all bids you've placed
- Shows cost for each bid
- Updated in real-time

## Auction Rules (Lowest Unique Bid)

**Goal:** Place the lowest unique bid
- You win if your bid is unique (no one else bid that amount) AND lowest
- Example: If bids are 5€, 3€, 3€, 7€:
  - Lowest unique = 5€
  - 3€ appears twice so not unique
  - 7€ is unique but not lowest
  - **Winner: The 5€ bidder**

## Game Strategy

### Defensive Strategy
- Place low bids early to stay ahead
- Watch for duplicate bids forming
- Adjust if another player matches your bid

### Aggressive Strategy
- Wait to see what prices others choose
- Try to find gaps where you can be unique
- Place a bid just lower than the current leader

### Analysis Strategy
- Use PAUSE to review the bid feed
- Study the statistics panel
- Predict likely bids and choose differently
- Watch for clustering around certain prices

## Real-Time Example Gameplay

```
START AUCTION
[Status] Demo file loaded with 30 players, user sees:

Bid 1-5 streaming in...
[  1] J01     ->  42€  (Current winner: J01 @ 42€)
[  2] J02     ->  54€  (Current winner: J01 @ 42€)
[  3] J03     ->  47€  (Current winner: J01 @ 42€)

[USER PLACES BID] Player: "You" -> 25€
[  4] (You)   ->  25€  (Current winner: YOU @ 25€)

[  5] J04     ->  45€  (Current winner: YOU @ 25€)
[  6] J05     ->  54€  (Current winner: YOU @ 25€)
[  7] J06     ->  40€  (Current winner: YOU @ 25€)

[USER PLACES BID] Player: "You" -> 10€
[  8] (You)   ->  10€  (Current winner: YOU @ 10€)

... continue until auction finishes ...

FINAL RESULT: YOU WIN with 10€!
```

## File Types Supported

### Single Round Files
- `lowbid_manche_demo.csv` - 30 players, 1 auction round
- All bids shown sequentially

### Multi-Round Files  
- `lowbid_multi_manches_500x40.csv` - 500 auction rounds, 40 players each
- Each round completes before moving to next
- Useful for testing strategy across multiple auctions

### Stress Test Files
- `lowbid_stress_200k.csv` - Large-scale auction with 200k+ bids
- Tests system performance
- Increase speed to see rapid bid streaming

## Tips & Tricks

1. **Use Pause Strategically**
   - Pause when you see interesting patterns
   - Plan your next bid before resuming

2. **Monitor Duplicates**
   - Watch the statistics for bid clustering
   - Avoid prices already used by multiple players

3. **Early Advantage**
   - Your first bid sets the baseline
   - Others might copy or beat you

4. **Last-Minute Bids**
   - Place strategic bids while auction is running
   - React to price trends in real-time

5. **Speed Matters**
   - Fast speed (100-300ms) = intense, quick thinking
   - Slow speed (1500-2000ms) = relaxed, strategic planning

## Statistics Explained

**Bids shown:** Number of bids processed so far vs total
- Example: "50/100" means 50 of 100 total bids have been shown

**Unique prices:** Count of distinct bid amounts (ignoring duplicates)
- Example: Bids [1, 2, 2, 3] = 3 unique prices (1, 2, 3)

**Min/Max:** Lowest and highest bid amounts seen
- Used to understand the range of bids

**Avg:** Average of all bids shown (sum / count)
- Shows typical bid amount

**Lowest Unique:** Lists smallest bid amounts that only 1 person bid
- First one shown = current winner

## Troubleshooting

**Q: "No bid data files found"**
- A: Ensure CSV files are in the `bid_data/` folder
- Check file names end in `.csv`

**Q: "Auction won't start"**
- A: Select a file from dropdown first
- Make sure the CSV file is valid

**Q: "My bid doesn't update winner"**
- A: Check for typing errors in bid amount
- Verify it's a valid integer

**Q: "Button says PAUSE but auction isn't running"**
- A: Click RESET to return to normal state
- Then select file and START AUCTION again

## Technical Info

- **Algorithm:** Binary Search Tree for O(n) winner calculation
- **Real-time Updates:** Python QTimer triggers bid display
- **Responsive UI:** Pause/Resume without losing data
- **Multi-threading Safe:** All bids processed in order

## Next Steps

1. **Try the Demo**
   - Start with `lowbid_manche_demo.csv`
   - Get familiar with the interface

2. **Speed Challenge**
   - Run at fastest speed (100ms)
   - Test your quick decision-making

3. **Multi-Round Tournament**
   - Load multi-round auction
   - See if you can win multiple rounds
   - Track your overall performance

4. **Stress Test**
   - Load 200k file at ultra-fast speed
   - Watch the system handle massive auctions
   - Analyze patterns across huge datasets

Enjoy your live auction experience!
