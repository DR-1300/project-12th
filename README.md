# Smart Parking Management System 

A high-performance, terminal-based CRUD (Create, Read, Update, and Delete) application designed to automate vehicle logistics, stay-duration tracking, and dynamic fee calculation. Built with a focus on relational data integrity and system efficiency.

## ⭐ Key Features
- **Real-Time Occupancy Tracking:** Monitors slot availability to prevent over-capacity.
- **Automated Fee Engine:** Calculates parking charges based on entry/exit timestamps.
- **Persistent Storage:** Integrated with MySQL for robust data handling and historical logging.
- **Secure Access:** Built-in authentication module for authorized personnel only.

## ⭐ Technical Stack
- **Language:** Python 3.14
- **Database:** MySQL (Relational Schema Design)
- **Libraries:** `mysql-connector-python`, `datetime`

## ⭐ System Architecture & "Mechanical Sympathy"
This project was engineered with a focus on how software interacts with data storage:
- **Relational Logic:** Used primary/foreign key constraints to ensure no orphaned vehicle records exist.
- **Query Optimization:** Implemented specific SQL queries to minimize latency during peak entry/exit times.
- **Data Integrity:** Enforced physical capacity limits via backend logic to ensure the system reflects the real-world environment accurately.

## ⭐ Getting Started

### Prerequisites
- Python 3.14 installed.
- MySQL Server running.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/DR-1300/your-repo-name.git](https://github.com/DR-1300/your-repo-name.git)