# **📦 LowBid Auction System**

**MVP Status:** v1.0 - Integrated Live & Advanced Analysis

**Group Members:** Noa Thams, Baptiste Lhors, Eleanor Cortes-Sommaro, Alexandre Hamard


## **🎯 Project Overview**

This application is a comprehensive auction system implementing the "lowest unique bid wins" mechanism with both interactive live auctions and advanced multi-round strategy analysis. The system features real-time bidding interfaces, AI-powered strategy simulation, and technical performance benchmarking using optimized BST data structures.

**Key Features:**
- **Live Auction Mode**: Real-time auction streaming with user participation, speed control, and live statistics
- **Advanced Analysis Mode**: Multi-round strategy simulation comparing AI bidding strategies
- **Technical Benchmarking**: Performance comparison of BST vs alternative implementations
- **Interactive GUI**: Tabbed PyQt5 interface for seamless switching between modes

## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**\
   git clone \[your-repo-link]\
   cd \[project-folder]

2. **Setup Virtual Environment:**\
   python -m venv .venv\
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**\
   pip install -r requirements.txt

4. **Run Application:**\
   python live_auction.py


## **🛠️ Technical Architecture**

### **Core Components:**

**Data Structures:**
- **Enhanced BST**: Binary Search Tree with successor/predecessor operations for advanced bidding strategies
- **AuctionBST**: Core auction logic with lowest unique bid detection
- **Alternative Implementations**: Dictionary and Heap-based auctions for benchmarking

**AI Strategies:**
- **ConservativeStrategy**: Low-risk bidding, avoids duplicates
- **AggressiveStrategy**: High-risk, high-reward bidding
- **AdaptiveStrategy**: Learns from previous rounds
- **RandomStrategy**: Baseline random bidding

**Simulation Engine:**
- **AuctionSimulator**: Multi-round simulation with comprehensive analysis
- **SimulationWorker**: Threaded execution for non-blocking UI
- **Performance Benchmarking**: Comparative analysis of implementations

**GUI Framework:**
- **PyQt5 Interface**: Tabbed application with Live Auction and Advanced Analysis modes
- **Real-time Updates**: Live bid feed, winner display, and statistics
- **Progress Tracking**: Simulation progress bars and result visualization

### **Architecture Diagram:**
```
┌─────────────────┐    ┌──────────────────┐
│   Live Auction  │    │ Advanced Analysis│
│     Interface   │    │    Interface     │
└─────────┬───────┘    └─────────┬────────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌─────────────────────┐
          │   AuctionSimulator  │
          │                     │
          │  ┌────────────────┐ │
          │  │   Strategies   │ │
          │  │ • Conservative │ │
          │  │ • Aggressive   │ │
          │  │ • Adaptive     │ │
          │  │ • Random       │ │
          │  └────────────────┘ │
          └─────────┬───────────┘
                    │
          ┌─────────────────────┐
          │   Data Structures   │
          │                     │
          │  ┌────────────────┐ │
          │  │ Enhanced BST   │ │
          │  │ Dictionary     │ │
          │  │ Heap           │ │
          │  └────────────────┘ │
          └─────────────────────┘
```

---

## **🧪 Testing & Validation**

### **Core Functionality Tests:**
```bash
# Test BST operations
python -c "from main import AuctionBST; bst = AuctionBST(); bst.insert(10, 'A'); print('Winner:', bst.find_winner())"

# Test strategy simulation
python -c "from main import AuctionSimulator; sim = AuctionSimulator(10, 10); sim.add_strategy(ConservativeStrategy, 5); sim.run_simulation()"
```

### **GUI Validation:**
- Launch application: `python main.py`
- Test Live Auction tab with sample data files
- Test Advanced Analysis tab with strategy simulation
- Verify real-time updates and statistics display

### **Performance Benchmarks:**
- BST vs Dictionary vs Heap implementation comparison
- Multi-round simulation performance analysis
- Memory usage and execution time metrics

## **📦 Dependencies**

This project is built using the following technologies:

**Core Framework:**
- **Python 3.8+**: Primary programming language
- **PyQt5**: GUI framework for interactive interface

**Data Processing:**
- **csv**: Built-in CSV file handling
- **collections**: Data structures and counters
- **typing**: Type hints for better code documentation

**Performance & Analysis:**
- **time**: Execution timing and benchmarking
- **random**: Random number generation for simulations

**Installation:**
```bash
pip install PyQt5
# All other dependencies are built-in Python modules
```

---

## **🔮 Future Roadmap (v2.0)**

**Enhanced Features:**
- **Network Multiplayer**: Real-time multiplayer auctions over network
- **Advanced Analytics**: Machine learning-based strategy prediction
- **Custom Strategy Builder**: User-defined bidding strategies
- **Historical Data Analysis**: Long-term auction trend analysis
- **Mobile Interface**: Cross-platform mobile application

**Technical Improvements:**
- **Database Integration**: Persistent auction history storage
- **API Endpoints**: RESTful API for external integrations
- **Real-time Notifications**: Push notifications for auction events
- **Advanced Visualization**: Interactive charts and graphs
- **Cloud Deployment**: Scalable cloud-based auction platform
