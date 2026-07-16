# Fitness Management Portal

Python console application for the CA group assignment.

## How to run in VS Code

1. Open this folder in VS Code.
2. Make sure Python 3.8 or above is installed.
3. Open a terminal in VS Code.
4. Run:

```bash
python app.py
```

The program creates `data/fitness_data.json` automatically on first run. The sample data includes at least 300 customers and 1500 class records across 6 months for statistics.

## Default logins

Admin:

- Username: `admin`
- Password: `admin123`

Sample customer:

- Username: `customer001`
- Password: `pass123`

## Files

- `app.py` - main Python program
- `docs/report_content.md` - report content draft
- `docs/user_guide.md` - user guide with sample screens
- `docs/flowchart.mmd` - Mermaid flowchart source
- `data/fitness_data.json` - generated automatically when the program runs

## Non-AI component suggestion

For the oral presentation, explain that the package deduction and booking validation feature was manually improved. In the code, this is handled by `book_class()` and checks:

- Customer has a matching package
- Class is not full
- Class is not in the past
- Customer has not already booked the same class
- Package count is deducted after confirmation
