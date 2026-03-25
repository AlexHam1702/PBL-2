import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel)
from PyQt5.QtCore import Qt

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

    def insert(self, price, player_name):
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

# --- INTERFACE GRAPHIQUE (PyQt6) ---

class AuctionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bst = AuctionBST()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lowest Unique Bid Wins - LowBid Admin")
        self.setGeometry(100, 100, 500, 400)

        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Entrées
        self.label = QLabel("Enter player name and bid price:")
        layout.addWidget(self.label)

        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Player Name")
        self.bid_input = QLineEdit()
        self.bid_input.setPlaceholderText("Bid Price (integer)")
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.bid_input)
        layout.addLayout(input_layout)

        # Boutons
        self.add_button = QPushButton("Add Bid")
        self.add_button.clicked.connect(self.add_bid)
        layout.addWidget(self.add_button)

        self.result_button = QPushButton("Calculate Winner")
        self.result_button.clicked.connect(self.display_winner)
        layout.addWidget(self.result_button)

        # Zone d'affichage
        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        layout.addWidget(self.display_area)

        central_widget.setLayout(layout)

    def add_bid(self):
        name = self.name_input.text()
        try:
            price = int(self.bid_input.text())
            if price < 0: raise ValueError
            
            # Calcul du coût (selon la formule du document)
            alpha = 100
            base_cost = 1.0
            cost = base_cost + (alpha / (price + 1))
            
            self.bst.insert(price, name)
            self.display_area.append(f"Added : {name} bid {price}€ (Cost : {cost:.2f}€)")
            
            self.name_input.clear()
            self.bid_input.clear()
        except ValueError:
            self.display_area.append("Error : Please enter a positive integer.")

    def display_winner(self):
        price, winner = self.bst.find_lowest_unique()
        if winner:
            self.display_area.append(f"\n🏆 Winner : {winner} with a bid of {price}€ !")
        else:
            self.display_area.append("\n❌ No unique winner at the moment.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AuctionApp()
    ex.show()
    sys.exit(app.exec())