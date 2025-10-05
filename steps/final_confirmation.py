import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_utils import switch_to_main_content, switch_to_iframe, wait_for_page_load
from config import IFRAME_ID, FORM_IFRAME_ID

def final_confirmation(driver):
    """Step 10: Check final signature, select disability, submit"""
    print('=' * 50)
    print('STEP 10: Final Confirmation')
    print('=' * 50)
    
    try:
        switch_to_main_content(driver)
        wait_for_page_load(driver)
        time.sleep(2)

        # Switch outer iframe
        if not switch_to_iframe(driver, iframe_id=IFRAME_ID):
            print('✗ Failed to switch to outer iframe')
            return False

        # Switch inner iframe
        if not switch_to_iframe(driver, iframe_id=FORM_IFRAME_ID):
            print('✗ Failed to switch to inner iframe')
            return False

        print('✓ Switched to inner iframe')
        wait = WebDriverWait(driver, 20)

        # Signature checkbox
        print('Clicking final signature checkbox...')
        sig_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "icims_f_signature")))
        sig_checkbox.click()
        time.sleep(1)

        # Disability radio
        print('Selecting Disability = No...')
        dis_radio = wait.until(EC.element_to_be_clickable((By.ID, "icims_f_Disability_No")))
        dis_radio.click()
        time.sleep(1)

        # Submit button
        print('Clicking final submit button...')
        submit_btn = wait.until(EC.element_to_be_clickable((By.NAME, "icims_submit")))
        submit_btn.click()
        print('✓ Step 10 submitted successfully!')

        switch_to_main_content(driver)
        time.sleep(2)
        return True

    except Exception as e:
        print(f'✗ Step 10 failed with error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False
