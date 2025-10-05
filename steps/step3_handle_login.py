import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_utils import input_text, human_like_click, wait_for_page_load
from config import EMAIL
import time


def check_for_login_redirect(driver, timeout=10):
    """
    Check if we got redirected to the login page
    Returns: True if on login page, False otherwise
    """
    try:
        current_url = driver.current_url
        print(f'Current URL: {current_url}')
        
        # Check if URL contains login.icims.com
        if "login.icims.com" in current_url:
            print('✓ Detected login redirect!')
            return True
        else:
            print('✓ No login redirect detected')
            return False
            
    except Exception as e:
        print(f'Error checking URL: {str(e)[:100]}')
        return False


def wait_for_url_change(driver, timeout=60):
    """
    Wait for URL to change (after CAPTCHA is solved)
    Returns: True if URL changed, False if timeout
    """
    print('=' * 50)
    print('⏳ Waiting for URL to change...')
    print('(Solve CAPTCHA if present)')
    print('=' * 50)
    
    original_url = driver.current_url
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        current_url = driver.current_url
        
        if current_url != original_url:
            print(f'✓ URL changed!')
            print(f'  From: {original_url}')
            print(f'  To: {current_url}')
            return True
        
        time.sleep(1)  # Check every second
    
    print(f'✗ URL did not change within {timeout} seconds')
    return False


def handle_login_page(driver):
    """
    Step 3: Handle the login page if redirected there
    Returns: True if successful, False otherwise
    """
    print('=' * 50)
    print('STEP 3: Handling Login Page')
    print('=' * 50)
    
    try:
        # IMPORTANT: Switch back to main content (we might still be in iframe)
        from utils.browser_utils import switch_to_main_content
        switch_to_main_content(driver)
        
        # Add extra wait for new page to fully load
        time.sleep(3)
        
        # Wait for page to load with longer timeout
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, 30)  # Increased timeout
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)  # Extra buffer
        
        print('✓ Page loaded')
        
        # Check if we're on the login page
        if not check_for_login_redirect(driver):
            print('✓ Not on login page, skipping this step')
            return True  # Not an error, just skip
        
        # We're on login page, enter email
        print(f'Entering email: {EMAIL}')
        
        # Try to find the username input
        if not input_text(
            driver,
            By.ID,
            "username",
            EMAIL,
            description="username/email field"
        ):
            # Try alternate selector
            if not input_text(
                driver,
                By.NAME,
                "username",
                EMAIL,
                description="username/email field (by name)"
            ):
                return False
        
        time.sleep(1)
        
        # Click Continue button
        print('Clicking Continue button...')
        
        # Try multiple selectors for Continue button
        selectors = [
            (By.CSS_SELECTOR, "button._button-login-id", "CSS class"),
            (By.CSS_SELECTOR, "button[data-action-button-primary='true']", "data attribute"),
            (By.XPATH, "//button[@type='submit' and contains(text(), 'Continue')]", "text content"),
            (By.CSS_SELECTOR, "button[type='submit'][name='action']", "submit button")
        ]
        
        clicked = False
        for by, value, desc in selectors:
            if human_like_click(driver, by, value, description=f"Continue button ({desc})"):
                clicked = True
                break
        
        if not clicked:
            print('✗ Could not find Continue button')
            return False
        
        print('✓ Step 3 completed successfully!')
        time.sleep(2)  # Wait for next page
        return True
        
    except Exception as e:
        print(f'✗ Step 3 failed with error: {str(e)}')
        return False


if __name__ == "__main__":
    # Test this step independently
    from utils.browser_utils import setup_driver
    from step1_click_apply import click_apply_button
    from step2_enter_email import enter_email
    
    driver = setup_driver()
    try:
        if click_apply_button(driver):
            if enter_email(driver):
                # Wait for URL change (manual CAPTCHA solving)
                wait_for_url_change(driver)
                
                # Handle login page
                success = handle_login_page(driver)
                if success:
                    input("Press Enter to continue...")
    finally:
        driver.quit()