# User Guide

## Starting the Program

Open the project in VS Code and run:

```bash
python app.py
```

The main menu is displayed:

```text
@@@@ Fitness Management Portal @@@@
1. Customer registration/Login
2. Admin Login
0. Exit
Enter option:
```

## Customer Login

Choose option `1`, then login with:

```text
Username: customer001
Password: pass123
```

After login, the member menu is displayed:

```text
@@@@ Members Main Menu @@@@
1. Buy package
2. View packages
3. Register for class
4. Logout
```

## Buying a Package

Choose option `1` in the member menu. Select one of the listed packages. The package is added automatically because payment is outside the system.

## Viewing Packages

Choose option `2` in the member menu. The system displays remaining lessons grouped by class type.

## Registering for Class

Choose option `3` in the member menu. The current week schedule appears. Enter a class number to book, `N` for next week, `P` for previous week, or `0` to return. The system only allows bookings up to four weeks in advance.

## Admin Login

Choose option `2` from the main menu and login with:

```text
Username: admin
Password: admin123
```

The admin menu is displayed:

```text
@@@ Admin System @@@
1. Class planner
2. View/Add trainer
3. View statistics
4. Logout
```

## Class Planner

The admin can view classes for a selected date, add a class, or delete a class. A class cannot be deleted if customers are already registered.

## Trainer Management

The admin can view trainer skills, hourly rate, and weekly availability. The admin can also add a new trainer.

## Statistics

Statistics can be viewed for:

- Last 4 weeks
- Last 3 months
- Last 12 months

The system displays registrations by class type, packages bought by class type, top five trainers, and estimated profit.
