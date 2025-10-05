import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_utils import switch_to_main_content, switch_to_iframe, wait_for_page_load
from config import JOB_SPECIFIC, IFRAME_ID

def fill_job_specific_questions(driver):
    """Step 8: Fill Job Specific Questions"""
    print('=' * 50)
    print('STEP 8: Filling Job Specific Questions') 
    print('=' * 50)
    
    try:
        switch_to_main_content(driver)
        wait_for_page_load(driver)
        time.sleep(2)
        print('✓ Page loaded after EEO submit')

        # Switch to iframe
        if not switch_to_iframe(driver, iframe_id=IFRAME_ID):
            print('✗ Failed to switch to Job Specific iframe')
            return False
        print('✓ Switched to Job Specific iframe')
        time.sleep(2)

        wait = WebDriverWait(driver, 20)

        # How did you hear about this position?
        print('Selecting "How did you hear about this position?"...')
        select1 = Select(wait.until(EC.presence_of_element_located((By.ID, "rcf3167"))))
        select1.select_by_visible_text(JOB_SPECIFIC["source"])
        time.sleep(1)

        # If Other, please specify
        if "source_other" in JOB_SPECIFIC and JOB_SPECIFIC["source_other"]:
            print('Filling "If Other, please specify"...')
            select2 = Select(wait.until(EC.presence_of_element_located((By.ID, "rcf3169"))))
            select2.select_by_visible_text(JOB_SPECIFIC["source_other"])
            time.sleep(1)

        # What allows you to work in the U.S.?
        print('Selecting "What allows you to work in the U.S.?"...')
        select3 = Select(wait.until(EC.presence_of_element_located((By.ID, "Q142"))))
        select3.select_by_visible_text(JOB_SPECIFIC["work_auth"])
        time.sleep(1)

        # Click Submit
        print('Clicking Submit button...')
        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "quesp_form_submit_i")))
        submit_btn.click()
        print('✓ Job Specific Questions submitted successfully!')

        switch_to_main_content(driver)
        time.sleep(2)
        return True

    except Exception as e:
        print(f'✗ Step 8 failed with error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False
