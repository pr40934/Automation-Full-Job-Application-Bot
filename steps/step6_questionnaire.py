import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import QUESTIONNAIRE, FORM_IFRAME_ID
import time

from utils.browser_utils import (
    switch_to_main_content,
    switch_to_nested_iframes,
    click_element,
    wait_for_page_load,
    switch_to_iframe
)

def select_radio_button(driver, radio_id, description="radio button"):
    """Select a radio button by ID with robust waiting"""
    try:
        wait = WebDriverWait(driver, 20)
        
        # Wait for element to be present
        print(f'Waiting for {radio_id}...')
        radio = wait.until(EC.presence_of_element_located((By.ID, radio_id)))
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
        time.sleep(1)
        
        # Use JavaScript click (more reliable for radio buttons)
        driver.execute_script("arguments[0].click();", radio)
        
        print(f'✓ Selected {description}')
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f'✗ Failed to select {description}')
        print(f'   Error: {str(e)[:200]}')
        return False


def check_checkbox(driver, checkbox_id, description="checkbox"):
    """Check a checkbox by ID"""
    try:
        wait = WebDriverWait(driver, 10)
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, checkbox_id)))
        
        if not checkbox.is_selected():
            checkbox.click()
            print(f'✓ Checked {description}')
        else:
            print(f'✓ {description} already checked')
        
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f'✗ Failed to check {description}: {str(e)[:100]}')
        return False


def answer_questionnaire(driver):
    """
    Step 6: Answer questionnaire questions
    Returns: True if successful, False otherwise
    """
    print('=' * 50)
    print('STEP 6: Answering Questionnaire')
    print('=' * 50)
    
    try:
        # Always start from main content
        switch_to_main_content(driver)
        time.sleep(5)

        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)
        print('✓ Questionnaire page loaded')

        # 🔁 Switch into nested iframes (outer → inner)
        print('Switching into nested questionnaire iframes...')
        iframe_chain = ["icims_content_iframe", "icims_formFrame"]  # adjust names if needed
        if not switch_to_nested_iframes(driver, iframe_chain):
            print('✗ Could not switch into nested iframes')
            return False

        print('✓ Switched into nested questionnaire iframes')
        time.sleep(3)

        # Question 1
        print('Answering: Are you legally authorized to work in the U.S.?')
        if QUESTIONNAIRE["work_in_us"] == "Yes":
            if not select_radio_button(driver, "icims_f_Work_In_US_Yes", "Work in US - Yes"):
                return False
        else:
            if not select_radio_button(driver, "icims_f_Work_In_US_No", "Work in US - No"):
                return False
        time.sleep(1)

        # Question 2
        print('Answering: Do you require immigration sponsorship?')
        if QUESTIONNAIRE["need_sponsorship"] == "Yes":
            if not select_radio_button(driver, "icims_f_Need_Sponsorship_Yes", "Need Sponsorship - Yes"):
                return False
        else:
            if not select_radio_button(driver, "icims_f_Need_Sponsorship_No", "Need Sponsorship - No"):
                return False
        time.sleep(1)

        # Question 3
        print('Answering: Are you at least 18 years old?')
        if QUESTIONNAIRE["over_18"] == "Yes":
            if not select_radio_button(driver, "icims_f_Over_18_Yes", "Over 18 - Yes"):
                return False
        else:
            if not select_radio_button(driver, "icims_f_Over_18_No", "Over 18 - No"):
                return False
        time.sleep(1)

        # Question 4
        print('Answering: Have you worked for this Company before?')
        if QUESTIONNAIRE["previously_employed"] == "Yes":
            if not select_radio_button(driver, "icims_f_Previously_Employed_Here_Yes", "Previously Employed - Yes"):
                return False
        else:
            if not select_radio_button(driver, "icims_f_Previously_Employed_Here_No", "Previously Employed - No"):
                return False
        time.sleep(1)

        # Question 5
        print('Answering: Do you have any relatives employed here?')
        if QUESTIONNAIRE["relatives_employed"] == "Yes":
            if not select_radio_button(driver, "icims_f_Any_Relatives_Employed_Here_Yes", "Relatives Employed - Yes"):
                return False
        else:
            if not select_radio_button(driver, "icims_f_Any_Relatives_Employed_Here_No", "Relatives Employed - No"):
                return False
        time.sleep(2)

        # Signature checkbox
        print('Checking signature agreement checkbox...')
        if QUESTIONNAIRE["signature_agree"]:
            if not check_checkbox(driver, "icims_f_signature", "Signature Agreement"):
                return False
        time.sleep(1)

        # Submit
        print('Clicking Submit button...')
        if not click_element(driver, By.NAME, "icims_submit", description="Submit button"):
            submit_btn = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit']")
            submit_btn.click()
        print('✓ Step 6 completed successfully!')
        
        switch_to_main_content(driver)
        time.sleep(3)
        return True

    except Exception as e:
        print(f'✗ Step 6 failed with error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test this step independently
    from utils.browser_utils import setup_driver
    from step1_click_apply import click_apply_button
    from step2_enter_email import enter_email
    from step3_handle_login import handle_login_page
    from step4_enter_password import enter_password
    from step5_fill_personal_info import fill_personal_info
    
    driver = setup_driver()
    try:
        if click_apply_button(driver):
            if enter_email(driver):
                if handle_login_page(driver):
                    if enter_password(driver):
                        if fill_personal_info(driver):
                            success = answer_questionnaire(driver)
                            if success:
                                input("Press Enter to continue...")
    finally:
        driver.quit()