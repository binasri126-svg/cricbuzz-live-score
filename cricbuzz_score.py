
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Cricbuzz live cricket page
URL = "https://www.cricbuzz.com/live-cricket-scores/173060/wi-vs-ban-2nd-test-west-indies-tour-of-bangladesh-2026"

# Save screenshot in the same folder as this Python file
PROJECT_FOLDER = Path(__file__).resolve().parent
SCREENSHOT_FILE = PROJECT_FOLDER / "score.png"

# False = visible browser; True = background browser
HEADLESS = False


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        try:
            print("Opening Cricbuzz...")
            page.goto(URL, wait_until="domcontentloaded", timeout=30000)

            print("Waiting for cricket score...")

            # Wait for the score section to appear
            page.wait_for_selector(
                "div.flex.flex-row.font-bold.text-xl",
                state="visible",
                timeout=20000
            )

            score_section = page.locator(
                "div.flex.flex-row.font-bold.text-xl"
            ).first

            score_text = score_section.inner_text().strip()
            print("\nLIVE CRICKET SCORE")
            print("-------------------------")
            print(score_text)

            # Save screenshot
            page.screenshot(path=str(SCREENSHOT_FILE))
            print(f"\nScreenshot saved: {SCREENSHOT_FILE}")

        except PlaywrightTimeoutError:
            print("\nNo live score found within the waiting time.")
            print("The match may not be live or Cricbuzz may not have loaded.")
            page.screenshot(path=str(SCREENSHOT_FILE))
            print(f"Screenshot saved: {SCREENSHOT_FILE}")

        except Exception as error:
            print(f"\nAn error occurred: {error}")

        finally:
            browser.close()


if __name__ == "__main__":
    main()
