import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_utils import input_text, human_like_click, wait_for_page_load
from config import PASSWORD
import time


def check_for_password_page(driver):
    """
    Check if we're on the password page
    Returns: True if on password page, False otherwise
    """
    try:
        current_url = driver.current_url
        print(f'Current URL: {current_url}')
        
        # Check if URL contains login/password
        if "login.icims.com/u/login/password" in current_url or "password" in current_url:
            print('✓ Detected password page!')
            return True
        else:
            print('✓ Not on password page')
            return False
            
    except Exception as e:
        print(f'Error checking URL: {str(e)[:100]}')
        return False


def enter_password(driver):
    """
    Step 4: Enter password and click LOG IN button
    Returns: True if successful, False otherwise
    """
    print('=' * 50)
    print('STEP 4: Entering Password')
    print('=' * 50)
    
    try:
        # Wait for page to load with longer timeout
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)  # Extra buffer
        
        print('✓ Page loaded')
        
        # Check if we're on the password page
        if not check_for_password_page(driver):
            print('✓ Not on password page, skipping this step')
            return True  # Not an error, just skip
        
        # Enter password
        print('Entering password...')
        
        # Try to find the password input
        if not input_text(
            driver,
            By.ID,
            "password",
            PASSWORD,
            description="password field"
        ):
            # Try alternate selector
            if not input_text(
                driver,
                By.NAME,
                "password",
                PASSWORD,
                description="password field (by name)"
            ):
                return False
        
        time.sleep(1)
        
        # Click LOG IN button
        print('Clicking LOG IN button...')
        
        # Try multiple selectors for LOG IN button
        selectors = [
            (By.CSS_SELECTOR, "button._button-login-password", "CSS class"),
            (By.CSS_SELECTOR, "button[data-action-button-primary='true']", "data attribute"),
            (By.XPATH, "//button[@type='submit' and contains(text(), 'LOG IN')]", "text content"),
            (By.CSS_SELECTOR, "button[type='submit'][name='action']", "submit button")
        ]
        
        clicked = False
        for by, value, desc in selectors:
            if human_like_click(driver, by, value, description=f"LOG IN button ({desc})"):
                clicked = True
                break
        
        if not clicked:
            print('✗ Could not find LOG IN button')
            return False
        
        print('✓ Step 4 completed successfully!')
        time.sleep(3)  # Wait for login to process
        return True
        
    except Exception as e:
        print(f'✗ Step 4 failed with error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Test this step independently
    from utils.browser_utils import setup_driver
    from step1_click_apply import click_apply_button
    from step2_enter_email import enter_email
    from step3_handle_login import handle_login_page
    
    driver = setup_driver()
    try:
        if click_apply_button(driver):
            if enter_email(driver):
                if handle_login_page(driver):
                    success = enter_password(driver)
                    if success:
                        input("Press Enter to continue...")
    finally:
        driver.quit()