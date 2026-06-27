import argparse
import sys
from tracker.storage import JSONStorage
from tracker.core import ExpenseTracker

def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="tracker",
        description="Expense Tracker CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # parser.add_argument(
    #     "--storage", type=str, default="expenses.json",
    #     help="Path to the JSON file for storing expenses."
    # )
    subparsers = parser.add_subparsers(
        dest="command", 
        required=True, 
        help="Available commands."
    )

    # Add expense subcommand setup
    add_parser = subparsers.add_parser("add", help="Add a new expense.")
    add_parser.add_argument("amount", type=float, help="Amount of the expense.")
    add_parser.add_argument("category", type=str, help="Category of the expense.")
    add_parser.add_argument("note", nargs="?", type=str, default="", help="Optional note for the expense.")

    # List expenses subcommand setup
    subparsers.add_parser("list", help="List all recorded expenses.")

    # Summary subcommand setup
    subparsers.add_parser("summary", help="Show total spending by category.")

    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Initialize the expense tracker
    storage = JSONStorage()
    try:
        tracker = ExpenseTracker(storage)
    except Exception as e:
        print(f"Failed to initialize expense tracker: {e}", file=sys.stderr)
        sys.exit(1)


    if args.command == "add":
        try:
            expense = tracker.add_expense(args.amount, args.category, args.note)
            print(f"Added expense: {expense}")
        except ValueError as e:
            print(f"Error adding expense: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "list":
        expenses = tracker.list_expenses()
        if not expenses:
            print("No expenses recorded yet.")
        else:
            for i, expense in enumerate(expenses):
                print(f"{i+1}. Amount: {expense.amount:>7.2f}, Category: {expense.category:<10}, Note: {expense.note}")
    elif args.command == "summary":
        for category, total in tracker.summary().items():
            print(f"Category: {category:<12} amount: ${total:.2f}")
        print(f"{'Total spent:':<12} ${tracker.total_expense():.2f}")
    return sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())