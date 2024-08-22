# Purdue Dining Court Menu RSS Feed Generator

This script generates an RSS feed for Purdue dining court menus, displaying current meals being served. It fetches data from the Purdue dining court API, formats it into an RSS feed, and includes each station's offerings with improved readability.

## Features

- Fetches dining court menu data for the current date.
- Includes only meals currently being served.
- Formats station names and their offerings with HTML for easy reading.
- Automatically runs as a cron job every 5 minutes (if configured).

## Requirements

- Python 3.x
- Python packages:
  - `requests`
  - `feedgen`

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/controllerking/purdue_menu_rss.git
cd purdue_menu_rss
```

### Step 2: Install Required Packages

Ensure you have Python 3 installed. Then, install the required Python packages:

```bash
pip3 install requests feedgen
```

### Step 3: Set Up the Script

Make sure the script is executable:

```bash
chmod +x purdue_menu_rss.py
```

### Step 4: (Optional) Set Up as a Cron Job

To run the script every 5 minutes, add a cron job:

1. Open the crontab file:

   ```bash
   crontab -e
   ```

2. Add the following line:

   ```bash
   */5 * * * * /usr/bin/python3 /path/to/your/purdue_menu_rss.py >> /path/to/your/purdue_menu_rss.log 2>&1
   ```

   Replace `/path/to/your/purdue_menu_rss.py` with the actual path to the script.

3. Save and exit the crontab editor.

### Step 5: Run the Script Manually (Optional)

You can run the script manually to test it:

```bash
python3 purdue_menu_rss.py
```

This will generate the RSS feed as `purdue_menu_rss.xml` in the current directory.

## Usage

The script generates an RSS feed that can be viewed in any RSS reader. The feed includes:

- **Title:** Dining Court Name - Meal Name - Meal Time
- **Description:** A list of stations and the food they offer, formatted with HTML for readability.

## Troubleshooting

- **Check the Log:** If the script doesn't work as expected, check the log file (`purdue_menu_rss.log`) for any error messages.
- **Ensure Permissions:** Make sure the script is executable (`chmod +x purdue_menu_rss.py`).
