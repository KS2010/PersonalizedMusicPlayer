"""
Entry point of the Personalized Music Player.
"""

from src.ui.main_window import MainWindow


def main():
    """Launch the application."""

    app = MainWindow()

    app.run()


if __name__ == "__main__":
    main()
