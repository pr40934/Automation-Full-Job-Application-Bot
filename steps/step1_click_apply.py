# steps/step1_click_apply.py - Step 1: Navigate to job page and click Apply

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from selenium.webdriver.common.by import By
# from utils.browser_utils import switch_to_iframe, wait_for_page_load, click_element
# from config import JOB_URL
# import time


# def click_apply_button(driver):
#     """
#     Step 1: Navigate to job page and click the Apply button
#     Returns: True if successful, False otherwise
#     """
#     print('=' * 50)
#     print('STEP 1: Clicking Apply Button')
#     print('=' * 50)
    
#     try:
#         # Navigate to job page
#         print(f'Navigating to: {JOB_URL}')
#         driver.get(JOB_URL)
        
#         # Wait for main page to load
#         if not wait_for_page_load(driver):
#             return False
        
#         # Switch to iframe
#         if not switch_to_iframe(driver):
#             return False
        
#         # Try multiple selectors for Apply button
#         selectors = [
#             (By.CSS_SELECTOR, "a.iCIMS_ApplyOnlineButton", "CSS selector"),
#             (By.XPATH, "//a[@title='Apply for this job online']", "title attribute"),
#             (By.XPATH, "//a[contains(text(), 'Apply')]", "text content")
#         ]
        
#         for by, value, desc in selectors:
#             if click_element(driver, by, value, description=f"Apply button ({desc})"):
#                 print('✓ Step 1 completed successfully!')
#                 time.sleep(2)  # Wait for next page to load
#                 return True
        
#         print('✗ Step 1 failed: Could not find Apply button')
#         return False
        
#     except Exception as e:
#         print(f'✗ Step 1 failed with error: {str(e)}')
#         return False


# if __name__ == "__main__":
#     # Test this step independently
#     from utils.browser_utils import setup_driver
    
#     driver = setup_driver()
#     try:
#         success = click_apply_button(driver)
#         if success:
#             input("Press Enter to continue...")
#     finally:
#         driver.quit()






# steps/step1_click_apply.py - Step 1: Navigate to job page and click Apply

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from utils.browser_utils import (
    switch_to_iframe, 
    switch_to_main_content, 
    wait_for_page_load, 
    human_like_click,
    random_mouse_movement
)
from config import JOB_URL, REDIRECT_URL
import time


def click_apply_button(driver):
    """
    Step 1: Navigate to job page and click the Apply button
    Returns: True if successful, False otherwise
    """
    print('=' * 50)
    print('STEP 1: Clicking Apply Button')
    print('=' * 50)
    
    try:
        # Navigate to job page
        print(f'Navigating to: {JOB_URL}')
        driver.get(JOB_URL)
        
        # Wait for main page to load
        if not wait_for_page_load(driver):
            return False
        
        # Switch to iframe
        if not switch_to_iframe(driver):
            return False
        
        # Do some random mouse movements to look human
        random_mouse_movement(driver)
        time.sleep(1)
        
        # Try multiple selectors for Apply button (using human-like clicking)
        selectors = [
            (By.CSS_SELECTOR, "a.iCIMS_ApplyOnlineButton", "CSS selector"),
            (By.XPATH, "//a[@title='Apply for this job online']", "title attribute"),
            (By.XPATH, "//a[contains(text(), 'Apply')]", "text content")
        ]
        
        for by, value, desc in selectors:
            if human_like_click(driver, by, value, description=f"Apply button ({desc})"):
                print('✓ Step 1 completed successfully!')
                time.sleep(2)  # Wait for next page to load
                
                # Switch back to main content before moving to next step
                switch_to_main_content(driver)
                return True

        # for by, value, desc in selectors:
        #     if human_like_click(driver, by, value, description=f"Apply button ({desc})"):
        #         print('✓ Step 1 completed successfully!')
        #         time.sleep(2)

        #         # Switch back to main content
        #         switch_to_main_content(driver)

        #         # Redirect to custom page
        #         print(f"Redirecting to custom page: {REDIRECT_URL}")
        #         driver.get(REDIRECT_URL)
        #         wait_for_page_load(driver)
        #         return True
        
        print('✗ Step 1 failed: Could not find Apply button')
        return False
        
    except Exception as e:
        print(f'✗ Step 1 failed with error: {str(e)}')
        return False


if __name__ == "__main__":
    # Test this step independently
    from utils.browser_utils import setup_driver
    
    driver = setup_driver()
    try:
        success = click_apply_button(driver)
        if success:
            input("Press Enter to continue...")
    finally:
        driver.quit()