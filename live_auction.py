import sys
import csv
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, 
                             QComboBox, QTableWidget, QTableWidgetItem, QSpinBox, QSlider)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor

# --- LOGIQUE ALGORITHMIQUE (BST) ---

class Node:
    def __init__(self, price, player_name):
        self.price = price
        self.players = [player_name]  # Liste pour gérer les doublons
        self.left = None
        self.right = None

class AuctionBST:
    def __init__(self):
        self.root = None
        self.all_bids = []  # Track all bids in insertion order

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
        """Parcours infixe pour trouver le plus petit prix avec un seul joueur."""
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
        """Reset the tree for a new round."""
        self.root = None
        self.all_bids = []

    def get_all_bids_sorted(self):
        """Return all bids sorted by price."""
        result = []
        self._inorder_traversal(self.root, result)
        return result

# --- INTERFACE GRAPHIQUE (PyQt5) - REAL-TIME AUCTION ---

class AuctionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bst = AuctionBST()
        self.current_bids = []  # All bids to display
        self.bid_index = 0  # Current bid being shown
        self.auction_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_bid)
        self.bid_speed = 500  # milliseconds between bids
        self.initUI()

    def initUI(self):
        self.setWindowTitle("LIVE AUCTION - Lowest Unique Bid Wins")
        self.setGeometry(50, 50, 1200, 800)

        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # === TOP SECTION: FILE SELECTION & CONTROLS ===
        file_layout = QHBoxLayout()
        file_label = QLabel("Select Auction File:")
        file_layout.addWidget(file_label)
        
        self.file_combo = QComboBox()
        self.load_bid_files()
        file_layout.addWidget(self.file_combo)
        
        self.start_button = QPushButton("START AUCTION")
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.start_button.clicked.connect(self.start_auction)
        file_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("PAUSE")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.pause_auction)
        file_layout.addWidget(self.pause_button)

        self.reset_button = QPushButton("RESET")
        self.reset_button.clicked.connect(self.reset_auction)
        file_layout.addWidget(self.reset_button)

        main_layout.addLayout(file_layout)

        # === SPEED CONTROL ===
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Auction Speed:")
        speed_layout.addWidget(speed_label)
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(100)
        self.speed_slider.setMaximum(2000)
        self.speed_slider.setValue(self.bid_speed)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(300)
        self.speed_slider.valueChanged.connect(self.update_speed)
        speed_layout.addWidget(self.speed_slider)
        
        self.speed_label = QLabel(f"{self.bid_speed}ms")
        speed_layout.addWidget(self.speed_label)
        speed_layout.addStretch()
        
        main_layout.addLayout(speed_layout)

        # === MAIN AUCTION AREA ===
        auction_layout = QHBoxLayout()

        # LEFT: Bid Feed
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("LIVE BID FEED:"))
        self.bid_feed = QTextEdit()
        self.bid_feed.setReadOnly(True)
        self.bid_feed.setMaximumWidth(400)
        bid_font = QFont("Courier")
        bid_font.setPointSize(10)
        self.bid_feed.setFont(bid_font)
        left_layout.addWidget(self.bid_feed)
        auction_layout.addLayout(left_layout)

        # CENTER: Current Winner & Stats
        center_layout = QVBoxLayout()
        
        # Winner display
        self.winner_label = QLabel("WAITING TO START...")
        winner_font = QFont()
        winner_font.setPointSize(20)
        winner_font.setBold(True)
        self.winner_label.setFont(winner_font)
        self.winner_label.setAlignment(Qt.AlignCenter)
        self.winner_label.setStyleSheet("background-color: #f0f0f0; padding: 20px; border-radius: 5px;")
        center_layout.addWidget(self.winner_label)

        # Auction info
        self.info_label = QLabel("Status: Ready")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("padding: 10px;")
        center_layout.addWidget(self.info_label)

        # Statistics
        stats_group_layout = QVBoxLayout()
        stats_group_layout.addWidget(QLabel("AUCTION STATISTICS:"))
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        stats_group_layout.addWidget(self.stats_display)
        center_layout.addLayout(stats_group_layout)

        auction_layout.addLayout(center_layout)

        # RIGHT: Player Bid Entry
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("PLACE YOUR BID:"))
        
        self.player_name_input = QLineEdit()
        self.player_name_input.setPlaceholderText("Your Player Name")
        right_layout.addWidget(self.player_name_input)

        self.player_bid_input = QLineEdit()
        self.player_bid_input.setPlaceholderText("Your Bid Amount")
        right_layout.addWidget(self.player_bid_input)

        self.place_bid_button = QPushButton("PLACE BID")
        self.place_bid_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        self.place_bid_button.clicked.connect(self.place_player_bid)
        right_layout.addWidget(self.place_bid_button)

        right_layout.addSpacing(20)
        right_layout.addWidget(QLabel("YOUR BIDS:"))
        self.player_bids_display = QTextEdit()
        self.player_bids_display.setReadOnly(True)
        right_layout.addWidget(self.player_bids_display)

        right_layout.addStretch()
        auction_layout.addLayout(right_layout)

        main_layout.addLayout(auction_layout)

        central_widget.setLayout(main_layout)

    def load_bid_files(self):
        """Load available CSV files from bid_data folder."""
        bid_data_path = Path(__file__).parent / "bid_data"
        if bid_data_path.exists():
            csv_files = sorted(list(bid_data_path.glob("*.csv")))
            for csv_file in csv_files:
                self.file_combo.addItem(csv_file.name, str(csv_file))

    def load_csv_data(self, filepath):
        """Load bids from CSV file."""
        try:
            bids = []
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        player_name = row['joueur'].strip()
                        price = int(row['prix'].strip())
                        bids.append((player_name, price))
                    except (ValueError, KeyError):
                        continue
            return bids
        except Exception as e:
            self.bid_feed.setText(f"Error loading file: {str(e)}")
            return []

    def start_auction(self):
        """Start the auction simulation."""
        if self.file_combo.count() == 0:
            self.bid_feed.setText("No bid data files found in bid_data folder.")
            return

        filepath = self.file_combo.currentData()
        self.current_bids = self.load_csv_data(filepath)

        if not self.current_bids:
            return

        # Reset state
        self.bst.clear()
        self.bid_index = 0
        self.auction_running = True
        self.bid_feed.clear()
        self.player_bids_display.clear()

        # Update UI
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.file_combo.setEnabled(False)

        # Start showing bids
        self.bid_feed.setText("AUCTION STARTED!\n" + "="*40 + "\n\n")
        self.timer.start(self.bid_speed)

    def show_next_bid(self):
        """Show the next bid in the auction."""
        if self.bid_index >= len(self.current_bids):
            # Auction finished
            self.end_auction()
            return

        player_name, price = self.current_bids[self.bid_index]
        self.bst.insert(price, player_name)
        self.bid_index += 1

        # Update bid feed
        self.bid_feed.append(f"[{self.bid_index:3d}] {player_name:6s} -> {price:3d}€")
        self.bid_feed.ensureCursorVisible()

        # Update winner and stats
        self.update_display()

    def update_display(self):
        """Update the winner display and statistics."""
        price, winner = self.bst.find_lowest_unique()

        # Update winner display
        if winner:
            self.winner_label.setText(f"CURRENT WINNER:\n{winner}\nBid: {price}€")
            self.winner_label.setStyleSheet("background-color: #FFD700; padding: 20px; border-radius: 5px; color: black;")
        else:
            self.winner_label.setText("NO UNIQUE WINNER YET")
            self.winner_label.setStyleSheet("background-color: #ff9800; padding: 20px; border-radius: 5px;")

        # Update info
        self.info_label.setText(f"Bids shown: {self.bid_index}/{len(self.current_bids)} | Unique prices: {len(self.bst.get_all_bids_sorted())}")

        # Update stats
        if self.bid_index > 0:
            sorted_bids = self.bst.get_all_bids_sorted()
            prices = [b[1] for b in self.current_bids[:self.bid_index]]
            
            stats_text = "Price Statistics:\n"
            stats_text += f"Bids shown: {self.bid_index}\n"
            stats_text += f"Unique prices: {len(sorted_bids)}\n"
            stats_text += f"Min: {min(prices)}€\n"
            stats_text += f"Max: {max(prices)}€\n"
            stats_text += f"Avg: {sum(prices) / len(prices):.1f}€\n\n"
            
            stats_text += "Lowest Unique:\n"
            for price_val, players in sorted_bids[:5]:
                is_unique = "UNIQUE" if len(players) == 1 else f"DUP({len(players)})"
                stats_text += f"{price_val}€ - {is_unique}\n"
            
            self.stats_display.setText(stats_text)

    def pause_auction(self):
        """Pause the auction."""
        if self.auction_running:
            self.timer.stop()
            self.auction_running = False
            self.pause_button.setText("RESUME")
        else:
            self.timer.start(self.bid_speed)
            self.auction_running = True
            self.pause_button.setText("PAUSE")

    def reset_auction(self):
        """Reset the auction."""
        self.timer.stop()
        self.auction_running = False
        self.bid_index = 0
        self.bst.clear()
        self.bid_feed.clear()
        self.player_bids_display.clear()
        self.winner_label.setText("WAITING TO START...")
        self.winner_label.setStyleSheet("background-color: #f0f0f0; padding: 20px; border-radius: 5px;")
        self.info_label.setText("Status: Ready")
        self.stats_display.clear()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("PAUSE")
        self.file_combo.setEnabled(True)

    def update_speed(self, value):
        """Update the auction speed."""
        self.bid_speed = value
        self.speed_label.setText(f"{value}ms")
        if self.auction_running:
            self.timer.setInterval(value)

    def place_player_bid(self):
        """Place a bid as the player."""
        name = self.player_name_input.text().strip()
        try:
            price = int(self.player_bid_input.text())
            if price < 0:
                raise ValueError("Bid must be positive")
            if not name:
                raise ValueError("Please enter your name")

            self.bst.insert(price, name)
            
            # Calculate cost
            alpha = 100
            base_cost = 1.0
            cost = base_cost + (alpha / (price + 1))

            # Display player bid
            self.player_bids_display.append(f"[{name}] placed {price}€ (Cost: {cost:.2f}€)")
            
            # Update display
            self.update_display()

            # Clear input
            self.player_bid_input.clear()

        except ValueError as e:
            self.player_bids_display.append(f"ERROR: {str(e)}")

    def end_auction(self):
        """End the auction when all bids are shown."""
        self.timer.stop()
        self.auction_running = False
        price, winner = self.bst.find_lowest_unique()

        # Final update
        self.bid_feed.append("\n" + "="*40)
        self.bid_feed.append("AUCTION ENDED!")

        if winner:
            self.bid_feed.append(f"\n[WINNER] {winner} with {price}€")
            self.winner_label.setText(f"AUCTION WINNER:\n{winner}\nBid: {price}€")
            self.winner_label.setStyleSheet("background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; font-size: 18px;")
        else:
            self.bid_feed.append("\n[NO UNIQUE WINNER]")
            self.winner_label.setText("NO UNIQUE WINNER")

        self.pause_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.file_combo.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AuctionApp()
    ex.show()
    sys.exit(app.exec())
