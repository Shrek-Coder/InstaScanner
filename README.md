# InstaScanner

**InstaScan** — a project for parsing data from Instagram. It provides tools for extracting information from profiles, posts, comments, and other publicly available information on Instagram.

What is described here:
**General Project Description**: A brief introduction to what the project does.
**Project Structure**: Explanation of what is in each directory.
**Features**: Description of the main components of the project.
**Installation**: How to install and set up the project, including dependencies and configurations.
**Usage**: Example of how to run the parser.
**Logs**: Information about log file locations for monitoring.
**Testing**: How to run the tests.
**Contributing**: Steps for those who want to participate in the development of the project.


# Project Structure
**The project is organized as follows**:
```
InstaScanner/
│
├── src/                   # Project source code
│   ├── parsers/           # Modules for parsing Instagram data
│   ├── utils/             # Utility functions for data handling and API operations
│   ├── configs/           # Configuration files
│       └── config.ini     # Main configuration file
│
├── data/                  # Directory for storing data
│   ├── raw/               # Raw data obtained during parsing
│   └── processed/         # Processed data
│
├── logs/                  # Parser logs
│
├── docs/                  # Project documentation
│
├── tests/                 # Tests for checking project functionality
│
├── scripts/               # Scripts for task automation
│
├── README.md              # Project documentation (this file)
├── .gitignore             # File to exclude unnecessary files from the repository
└── requirements.txt       # List of project dependencies
```

#   Features
**The InstaScan project includes the following main components**:

**Parsers**
Modules for parsing data from various Instagram sections: user profiles, posts, comments, etc.

**Utilities**
Helper functions for working with the Instagram API, processing and saving data, handling logs, and managing configurations.

**Configurations**
Main parameters for project setup (e.g., API keys, timeouts, data paths) are stored in the config.ini file.

# Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Shrek-Coder/InstaScanner.git
   cd InstaScanner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up configurations in the src/configs/config.ini file: `src/configs/config.ini`:
   ```ini
   [Instagram]
   username = 
   password = 
   ```

# Usage

To run the parser and retrieve Instagram user data, execute:

```
python main.py
```
You can configure the types of data to parse through the configuration file.


# Logs

All actions and possible errors are logged in the `logs/` directory. These logs will help you monitor the parsing process and identify errors when working with the Instagram API.

# Testing
Tests for the project are located in the `tests/` directory. To run all tests, use:

```
pytest tests/
```