from core.browser_manager import launch_browser
from core.logger import get_logger
from core.human_behaviour import simulate_scroll, simulate_mouse_move


def run_demo():
    logger = get_logger()
    driver = launch_browser(headless=False)

    driver.get("https://httpbin.org/ip")  # 👈 see IP inside real browser

    simulate_mouse_move(driver)
    simulate_scroll(driver)

    try:
        input("✅ Press Enter to close browser...")
    finally:
        driver.quit()


if __name__ == "__main__":
    run_demo()
