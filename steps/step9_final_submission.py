import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_utils import switch_to_main_content, switch_to_iframe, wait_for_page_load
from config import PERSONAL_INFO, IFRAME_ID, FORM_IFRAME_ID

def final_submission(driver):
    """Step 9: Final Step - Veteran info, Date, Signature, Submit"""
    print('=' * 50)
    print('STEP 9: Final Submission')
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

        # Select Veteran radio
        print('Selecting Veteran radio...')
        vet_radio = wait.until(EC.element_to_be_clickable((By.ID, "icims_f_Veteran_NotProtectedVeteran")))
        vet_radio.click()
        time.sleep(1)

        # Enter Name
        print('Entering Name...')
        name_input = wait.until(EC.presence_of_element_located((By.ID, "icims_f_Name")))
        full_name = f"{PERSONAL_INFO['first_name']} {PERSONAL_INFO['last_name']}"
        name_input.clear()
        name_input.send_keys(full_name)
        time.sleep(1)

        # Get current date
        now = datetime.now()
        current_month = f"{now.month:02d}"
        current_day = str(now.day)
        current_year = str(now.year)

        # Month
        print('Selecting Month...')
        month_select = Select(wait.until(EC.presence_of_element_located((By.ID, "icims_f_Date_Month"))))
        month_select.select_by_value(current_month)
        time.sleep(1)

        # Day
        print('Selecting Day...')
        day_select = Select(wait.until(EC.presence_of_element_located((By.ID, "icims_f_Date_Date"))))
        day_select.select_by_value(current_day)
        time.sleep(1)

        # Year
        print('Entering Year...')
        year_input = wait.until(EC.presence_of_element_located((By.ID, "icims_f_Date_Year")))
        year_input.clear()
        year_input.send_keys(current_year)
        time.sleep(1)

        # Signature checkbox
        print('Clicking signature checkbox...')
        sig_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "icims_f_signature")))
        sig_checkbox.click()
        time.sleep(1)

        # Submit button
        print('Clicking Submit button...')
        submit_btn = wait.until(EC.element_to_be_clickable((By.NAME, "icims_submit")))
        submit_btn.click()
        print('✓ Final step submitted successfully!')

        switch_to_main_content(driver)
        time.sleep(2)
        return True

    except Exception as e:
        print(f'✗ Step 9 failed with error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False
