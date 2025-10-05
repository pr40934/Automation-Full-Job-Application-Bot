# steps/step5_fill_personal_info.py - Step 5: Fill personal information form

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_utils import (
    clear_and_input_text,
    select_dropdown_by_partial_text,
    select_custom_dropdown,
    find_element_by_partial_id,
    switch_to_iframe,
    switch_to_main_content,
    wait_for_page_load
)
from config import PERSONAL_INFO, RESUME_PATH , EMAIL, PASSWORD
# from config import 
import time


def fill_personal_info(driver):
    """
    Step 5: Fill personal information form
    Returns: True if successful, False otherwise
    """
    print('=' * 50)
    print('STEP 5: Filling Personal Information')
    print('=' * 50)
    
    try:
        # Switch back to main content first
        switch_to_main_content(driver)
        
        # Wait for page to load
        time.sleep(3)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)
        
        print('✓ Page loaded')
        
        # IMPORTANT: Switch to iframe - the form is inside it!
        print('Switching to form iframe...')
        if not switch_to_iframe(driver):
            print('✗ Could not switch to iframe')
            return False
        
        print('✓ Switched to form iframe')
        time.sleep(1)

        # Toggle resume checkbox BEFORE entering name
        print("Handling resume upload checkbox...")
        from utils.browser_utils import toggle_checkbox

        # Upload Resume
        try:
            print("Uploading resume...")
            resume_input = driver.find_element(By.ID, "PortalProfileFields.Resume_File")
            resume_input.send_keys(RESUME_PATH)
            print("✓ Resume uploaded successfully")
        except Exception as e:
            print(f"⚠️ Resume upload failed: {e}, continuing...")

        
        print("Filling login credentials...")
        try:
            # Login / Email
            login_input = driver.find_element(By.ID, "PersonProfileFields.Login")
            login_input.clear()
            login_input.send_keys(EMAIL)
            print(f"✓ Email/Login entered: {EMAIL}")

            # Password
            password_input = driver.find_element(By.ID, "PersonProfileFields.Password")
            password_input.clear()
            password_input.send_keys(PASSWORD)

            # Confirm Password
            password_confirm_input = driver.find_element(By.ID, "PersonProfileFields.Password_Confirm")
            password_confirm_input.clear()
            password_confirm_input.send_keys(PASSWORD)

            print("✓ Password and confirm password entered successfully")
            time.sleep(1)
        except Exception as e:
            print(f"✗ Failed to fill login/password: {e}")
            return False
        
        # Fill First Name
        print(f'Filling first name: {PERSONAL_INFO["first_name"]}')
        if not clear_and_input_text(
            driver,
            By.ID,
            "PersonProfileFields.FirstName",
            PERSONAL_INFO["first_name"],
            description="First Name"
        ):
            return False
        
        time.sleep(2)
        
        # Fill Last Name
        print(f'Filling last name: {PERSONAL_INFO["last_name"]}')
        if not clear_and_input_text(
            driver,
            By.ID,
            "PersonProfileFields.LastName",
            PERSONAL_INFO["last_name"],
            description="Last Name"
        ):
            return False
        
        time.sleep(2)

        login_input = driver.find_element(By.ID, "PersonProfileFields.Email")
        login_input.clear()
        login_input.send_keys(EMAIL)
        print(f"✓ Email/Login entered: {EMAIL}")
        
        # Select Phone Type (using partial ID since it has dynamic number)
        # Select Phone Type (prefer real <select> to avoid picking label)
        print(f'Selecting phone type: {PERSONAL_INFO["phone_type"]}')

        phone_type_element = find_element_by_partial_id(driver, "PersonProfileFields.PhoneType", tag="select")

        if phone_type_element:
            phone_type_id = phone_type_element.get_attribute("id")
            print(f'Found phone type <select> with ID: {phone_type_id}')
            
            if not select_dropdown_by_partial_text(
                driver,
                By.ID,
                phone_type_id,
                PERSONAL_INFO["phone_type"],
                description="Phone Type"
            ):
                return False
        else:
            print('✗ Could not find Phone Type <select> dropdown')
            return False
        
        # Fill Phone Number (using partial ID)
        print(f'Filling phone number: {PERSONAL_INFO["phone_number"]}')
        # phone_number_element = find_element_by_partial_id(driver, "_PersonProfileFields.PhoneNumber")
        
        phone_number_element = driver.find_element(
            By.XPATH,
            "//input[contains(@id,'PersonProfileFields.PhoneNumber')]"
        )

        phone_number_id = phone_number_element.get_attribute("id")
        if not clear_and_input_text(
            driver,
            By.ID,
            phone_number_id,
            PERSONAL_INFO["phone_number"],
            description="Phone Number"
        ):
            return False

        time.sleep(2)
        
        # Fill Phone Extension (using partial ID)
        print(f'Filling phone extension: {PERSONAL_INFO["phone_extension"]}')
        # phone_ext_element = find_element_by_partial_id(driver, "_PersonProfileFields.PhoneExtension")
        phone_ext_element = driver.find_element(
            By.XPATH,
            "//input[contains(@id,'PersonProfileFields.PhoneExtension')]"
        )
        
        phone_ext_id = phone_ext_element.get_attribute("id")
        if not clear_and_input_text(
            driver,
            By.ID,
            phone_ext_id,
            PERSONAL_INFO["phone_extension"],
            description="Phone Extension"
        ):
            return False
        

        # ===== Address Section =====
        print("Filling Address Section...")

        # Select Address Type (Home)
        addr_type_el = driver.find_element(By.XPATH, "//select[contains(@id,'PersonProfileFields.AddressType')]")
        addr_type_id = addr_type_el.get_attribute("id")
        if not select_dropdown_by_partial_text(driver, By.ID, addr_type_id, "Home", description="Address Type"):
            return False
        time.sleep(2)

        # Address Street
        addr_street_el = driver.find_element(By.XPATH, "//input[contains(@id,'PersonProfileFields.AddressStreet1')]")
        addr_street_id = addr_street_el.get_attribute("id")
        if not clear_and_input_text(driver, By.ID, addr_street_id, PERSONAL_INFO["address_street"], description="Address Street"):
            return False
        time.sleep(2)

        # Address City
        addr_city_el = driver.find_element(By.XPATH, "//input[contains(@id,'PersonProfileFields.AddressCity')]")
        addr_city_id = addr_city_el.get_attribute("id")
        if not clear_and_input_text(driver, By.ID, addr_city_id, PERSONAL_INFO["address_city"], description="Address City"):
            return False
        time.sleep(2)

        # Address Zip
        addr_zip_el = driver.find_element(By.XPATH, "//input[contains(@id,'PersonProfileFields.AddressZip')]")
        addr_zip_id = addr_zip_el.get_attribute("id")
        if not clear_and_input_text(driver, By.ID, addr_zip_id, PERSONAL_INFO["address_zip"], description="Address Zip"):
            return False
        time.sleep(2)

        # --- Select Country (Custom Dropdown) ---
        print("Selecting Country: India")
        try:
            # Find the visible dropdown trigger (the <a> tag)
            country_trigger = driver.find_element(
                By.XPATH, 
                "//a[contains(@id,'AddressCountry_icimsDropdown')]"
            )
            # Scroll into view and click
            driver.execute_script("arguments[0].scrollIntoView(true);", country_trigger)
            time.sleep(2)
            country_trigger.click()
            time.sleep(1)

            # Use the search box that appears
            search_box = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'AddressCountry_icimsDropdown_ctnr')]//input[@class='dropdown-search']")
                )
            )
            search_box.clear()
            search_box.send_keys("India")
            time.sleep(1)
            
            # Click the India option
            india_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//li[@role='option' and @title='India']"))
            )
            india_option.click()
            print("✓ Country selected: India")
            time.sleep(1)
        except Exception as e:
            print(f"✗ Failed to select country: {e}")
            return False

        # --- Select State (Custom Dropdown) ---
        print("Selecting State: Andhra Pradesh")
        try:
            # Find the visible state dropdown trigger
            state_trigger = driver.find_element(
                By.XPATH,
                "//a[contains(@id,'AddressState_icimsDropdown')]"
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", state_trigger)
            time.sleep(2)
            state_trigger.click()
            time.sleep(1)

            # Use the search box
            search_box = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'AddressState_icimsDropdown_ctnr')]//input[@class='dropdown-search']")
                )
            )
            search_box.clear()
            search_box.send_keys("Andhra Pradesh")
            time.sleep(1)

            # Click the option
            ap_option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//li[@role='option' and @title='Andhra Pradesh']"))
            )
            ap_option.click()
            print("✓ State selected: Andhra Pradesh")
            time.sleep(1)
        except Exception as e:
            print(f"✗ Failed to select state: {e}")
            return False


        # --- Select "How did you hear about us?" ---
        print("Selecting: How did you hear about us -> Indeed.com")
        if not select_dropdown_by_partial_text(
            driver,
            By.ID,
            "rcf3048",
            "Indeed.com",
            description="How did you hear about us"
        ):
            print("✗ Failed to select 'Indeed.com'")
            return False
        print("✓ Selected 'Indeed.com'")

        time.sleep(2)

        # --- Select "Are you willing to relocate?" ---
        print("Selecting: Are you willing to relocate -> Yes")
        try:
            relocate_select = driver.find_element(
                By.XPATH, "//select[@data-label='Are you willing to relocate?']"
            )
            driver.execute_script("arguments[0].value = 'Yes'; arguments[0].dispatchEvent(new Event('change'));", relocate_select)
            print("✓ Selected 'Yes' for 'Are you willing to relocate'")
        except Exception as e:
            print(f"✗ Failed to set 'Are you willing to relocate': {e}")
            return False

        time.sleep(3)

        # --- Click Update Profile button ---
        print("Clicking Update Profile button...")
        update_btn = driver.find_element(By.ID, "cp_form_submit_i")
        update_btn.click()
        print("✓ Clicked Update Profile successfully")
        
        print('✓ Step 5 completed successfully!')
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f'✗ Step 5 failed with error: {str(e)}')
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
    
    driver = setup_driver()
    try:
        if click_apply_button(driver):
            if enter_email(driver):
                if handle_login_page(driver):
                    if enter_password(driver):
                        success = fill_personal_info(driver)
                        if success:
                            input("Press Enter to continue...")
    finally:
        driver.quit()