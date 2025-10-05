import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from utils.browser_utils import switch_to_iframe, wait_for_page_load, input_text, click_element
from config import EMAIL
import time


def enter_email(driver):
    """
    Step 2: Enter email address and click Next button
    Returns: True if successful, False otherwise
    """
    print('=' * 50)
    print('STEP 2: Entering Email')
    print('=' * 50)
    
    try:
        # Wait for the new page to load
        if not wait_for_page_load(driver):
            return False
        
        # Switch to iframe (the new page also has an iframe)
        if not switch_to_iframe(driver):
            return False
        
        # Enter email
        print(f'Entering email: {EMAIL}')
        if not input_text(
            driver,
            By.ID,
            "email",
            EMAIL,
            description="email field"
        ):
            return False
        
        time.sleep(1)
        
        # Click the Next/Submit button
        if not click_element(
            driver,
            By.ID,
            "enterEmailSubmitButton",
            description="Next button"
        ):
            return False
        
        print('✓ Step 2 completed successfully!')
        time.sleep(2)  # Wait for next page
        return True
        
    except Exception as e:
        print(f'✗ Step 2 failed with error: {str(e)}')
        return False


if __name__ == "__main__":
    # Test this step independently (requires Step 1 to run first)
    from utils.browser_utils import setup_driver
    from step1_click_apply import click_apply_button
    
    driver = setup_driver()
    try:
        if click_apply_button(driver):
            success = enter_email(driver)
            if success:
                input("Press Enter to continue...")
    finally:
        driver.quit()