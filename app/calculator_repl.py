########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory
from app.color import print_success, print_error, print_info, print_warning


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff - Perform calculations")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print_info("History saved successfully.")
                    except Exception as e:
                        print_warning(f"Warning: Could not save history: {e}")
                    print_info("Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print_warning("No calculations in history")
                    else:
                        print_info("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print_info("History cleared")
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print_success("Operation undone")
                    else:
                        print_info("Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print_success("Operation redone")
                    else:
                        print_info("Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print_success("History saved successfully")
                    except Exception as e:
                        print_error(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print_success("History loaded successfully")
                    except Exception as e:
                        print_error(f"Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_divide', 'percent', 'abs_diff']:
                    # Perform the specified arithmetic operation
                    try:
                        print_info("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print_info("Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print_info("Operation cancelled")
                            continue

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print_success(f"\nResult: {result}")
                    except (ValidationError, OperationError) as e: # pragma: no cover
                        # Handle known exceptions related to validation or operation errors
                        print_error(f"Error: {e}")
                    except Exception as e: # pragma: no cover
                        # Handle any unexpected exceptions
                        print_error(f"Unexpected error: {e}")
                    continue

                # Handle unknown commands
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print_info("\nOperation cancelled")
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print_info("\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print_error(f"Error: {e}")
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print_error(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
