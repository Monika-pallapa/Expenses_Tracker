## Personal Expense Tracker 💸

A simple, modern desktop application built with Python and Tkinter to help you record and manage personal expenses.
It includes a dashboard, expense search, and tools to add, edit, and delete records.
✨ Features

---

Dashboard cards showing total spending, number of expenses, highest expense, and top spending category
Add expenses with a name, amount, category, and automatically recorded date
View expenses in a clean table
Live search by expense name or category
Edit expenses when details change
Delete expenses with a confirmation prompt
Input validation to prevent blank names and invalid or non-positive amounts
Persistent storage using a local JSON file

## 🛠️ Built With

Python 3
Tkinter — desktop graphical user interface
JSON — local expense storage
datetime — date handling
No third-party Python packages are required. Tkinter is included with many Python installations; on some Linux systems it may need to be installed separately.

## 📁 Project Structure

Personal-Expense-Tracker/
├── tracker.py
├── expenses.json
└── README.md
tracker.py — application code
expenses.json — saved expense data; created when the app saves expenses
Note: Keep tracker.py and expenses.json in the same folder so the application can load your saved expenses.
🚀 Getting Started

1. Install Python
   Install Python 3 from python.org if it is not already installed.
2. Download or clone the repository
   git clone https://github.com/YOUR-USERNAME/Personal-Expense-Tracker.git
   cd Personal-Expense-Tracker
   Replace YOUR-USERNAME with your GitHub username. Alternatively, download the repository as a ZIP and extract it.
3. Run the application
   Open a terminal in the project folder and run:
   python tracker.py
   On some systems, use:
   python3 tracker.py
   A desktop window should open.
   🧭 How to Use
   Launch the application.
   Click + Add Expense.
   Enter the expense name and amount, then choose a category.
   Select an expense in the table to edit or delete it.
   Type in the search box to filter by expense name or category.
   Use the dashboard cards to review your spending summary.
   Available categories are Food, Travel, Shopping, Bills, and Other.
   💾 Data and Privacy
   Expenses are stored locally in expenses.json. The app does not need an online account or send your expense records to a server.
   Back up expenses.json if you want to keep your records. Do not commit personal financial information to a public GitHub repository. For a public demo, use sample data or omit your personal expenses.json file.
   🧪 Troubleshooting
   The window does not open: Check that Python and Tkinter are installed.
   python is not recognized: Try python3 or use the Python launcher available on your system.
   My expenses are missing: Confirm that expenses.json is in the same folder as tracker.py.
   The app opens with no records: The JSON file may be empty or contain invalid JSON. Make a backup before editing or replacing it.
   🔮 Possible Future Improvements
   Monthly spending charts
   Date-range filtering
   Export expenses to CSV
   Monthly budgets and budget alerts
   Dark mode
   Automated tests
   🤝 Contributing
   Suggestions and improvements are welcome. Fork the repository, make your changes, and open a pull request.
   📄 License
   This project is available under the MIT License. If you choose this license, add a LICENSE file containing the MIT License text and your copyright year/name.
   Made with Python 🐍
