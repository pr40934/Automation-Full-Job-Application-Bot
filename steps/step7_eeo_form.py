import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_utils import switch_to_main_content, switch_to_iframe, wait_for_page_load
from config import EEO_INFO, IFRAME_ID

def fill_eeo_form(driver):
    """Step 7: Fill EEO / Voluntary Information form"""
    print('=' * 50)
    print('STEP 7: Filling EEO / Voluntary Information')
    print('=' * 50)
    
    try:
        switch_to_main_content(driver)
        wait_for_page_load(driver)
        time.sleep(3)
        print('✓ Page loaded after questionnaire submit')

        # Switch to single iframe (same outer)
        if not switch_to_iframe(driver, iframe_id=IFRAME_ID):
            print('✗ Failed to switch to EEO iframe')
            return False
        print('✓ Switched to EEO iframe')
        time.sleep(2)

        wait = WebDriverWait(driver, 20)

        # Gender
        print('Selecting Gender...')
        gender_select = Select(wait.until(EC.presence_of_element_located((By.ID, "CandProfileFields.Gender"))))
        gender_select.select_by_visible_text(EEO_INFO["gender"])
        time.sleep(1)

        # Race
        print('Selecting Race...')
        race_select = Select(wait.until(EC.presence_of_element_located((By.ID, "CandProfileFields.Race"))))
        race_select.select_by_visible_text(EEO_INFO["race"])
        time.sleep(1)

        # Disability
        print('Selecting Disability...')
        dis_select = Select(wait.until(EC.presence_of_element_located((By.ID, "CandProfileFields.Disability"))))
        dis_select.select_by_visible_text(EEO_INFO["disability"])
        time.sleep(1)

        # Veteran
        print('Selecting Veteran...')
        vet_select = Select(wait.until(EC.presence_of_element_located((By.ID, "CandProfileFields.Veteran"))))
        vet_select.select_by_visible_text(EEO_INFO["veteran"])
        time.sleep(2)

        # Submit
        print('Clicking Submit button...')
        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "eeop_form_submit_i")))
        submit_btn.click()
        print('✓ EEO form submitted successfully!')

        switch_to_main_content(driver)
        time.sleep(3)
        return True

    except Exception as e:
        print(f'✗ Step 7 failed with error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False
