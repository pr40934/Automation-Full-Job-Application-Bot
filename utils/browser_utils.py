from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BROWSER_OPTIONS, DEFAULT_WAIT, IFRAME_ID, TYPING_DELAY


def setup_driver():
    """Initialize and configure the Chrome WebDriver"""
    options = webdriver.ChromeOptions()
    
    if BROWSER_OPTIONS.get("start_maximized"):
        options.add_argument("--start-maximized")
    
    if BROWSER_OPTIONS.get("headless"):
        options.add_argument("--headless")
    
    if BROWSER_OPTIONS.get("disable_automation"):
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def switch_to_iframe(driver, iframe_id=IFRAME_ID, timeout=DEFAULT_WAIT):
    """Switch to an iframe by ID"""
    try:
        wait = WebDriverWait(driver, timeout)
        print(f'Looking for iframe: {iframe_id}...')
        iframe = wait.until(EC.presence_of_element_located((By.ID, iframe_id)))
        driver.switch_to.frame(iframe)
        print(f'✓ Switched to iframe: {iframe_id}')
        return True
    except Exception as e:
        print(f'✗ Failed to switch to iframe: {str(e)[:100]}')
        return False


def switch_to_main_content(driver):
    """Switch back to main content from iframe"""
    try:
        driver.switch_to.default_content()
        print('✓ Switched back to main content')
        return True
    except Exception as e:
        print(f'✗ Failed to switch to main content: {str(e)[:100]}')
        return False


def wait_for_page_load(driver, timeout=DEFAULT_WAIT):
    """Wait for page to load"""
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1)  # Additional buffer
        print('✓ Page loaded')
        return True
    except Exception as e:
        print(f'✗ Page load failed: {str(e)[:100]}')
        return False


def click_element(driver, by, value, timeout=DEFAULT_WAIT, description="element"):
    """Generic function to wait for and click an element"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        print(f'✓ Clicked {description}')
        time.sleep(1)
        return True
    except Exception as e:
        print(f'✗ Failed to click {description}: {str(e)[:100]}')
        return False


def input_text(driver, by, value, text, timeout=DEFAULT_WAIT, description="input", human_like=True):
    """Generic function to input text into a field"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        element.clear()
        
        # Type like a human if enabled
        if human_like and BROWSER_OPTIONS.get("add_human_delays", False):
            for char in text:
                element.send_keys(char)
                time.sleep(TYPING_DELAY + random.uniform(0, 0.05))  # Random variation
        else:
            element.send_keys(text)
        
        print(f'✓ Entered text into {description}')
        return True
    except Exception as e:
        print(f'✗ Failed to input text into {description}: {str(e)[:100]}')
        return False


def clear_and_input_text(driver, by, value, text, timeout=DEFAULT_WAIT, description="input", human_like=True):
    """Clear input field completely and then enter text"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        
        # Clear the field multiple ways to ensure it's empty
        element.clear()
        time.sleep(0.2)
        
        # Select all and delete (backup clear)
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        time.sleep(0.2)
        
        # Now type the new text
        if human_like and BROWSER_OPTIONS.get("add_human_delays", False):
            for char in text:
                element.send_keys(char)
                time.sleep(TYPING_DELAY + random.uniform(0, 0.05))
        else:
            element.send_keys(text)
        
        print(f'✓ Cleared and entered text into {description}')
        return True
    except Exception as e:
        print(f'✗ Failed to clear and input text into {description}: {str(e)[:100]}')
        return False


def select_dropdown_by_text(driver, by, value, text, timeout=DEFAULT_WAIT, description="dropdown"):
    """Select an option from dropdown by visible text"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        
        select = Select(element)
        select.select_by_visible_text(text)
        
        print(f'✓ Selected "{text}" from {description}')
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f'✗ Failed to select from {description}: {str(e)[:100]}')
        return False


def select_dropdown_by_partial_text(driver, by, value, partial_text, timeout=DEFAULT_WAIT, description="dropdown"):
    """Select an option from dropdown by partial visible text match"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        
        select = Select(element)
        
        # Find option that contains the partial text
        for option in select.options:
            if partial_text.lower() in option.text.lower():
                select.select_by_visible_text(option.text)
                print(f'✓ Selected "{option.text}" from {description}')
                time.sleep(0.5)
                return True
        
        print(f'✗ Could not find option containing "{partial_text}" in {description}')
        return False
    except Exception as e:
        print(f'✗ Failed to select from {description}: {str(e)[:100]}')
        return False


def find_element_by_partial_id(driver, partial_id, timeout=DEFAULT_WAIT, tag=None):
    """
    Find element whose ID contains the partial_id string
    If tag is provided (e.g. 'select'), only match that specific tag
    """
    try:
        wait = WebDriverWait(driver, timeout)
        if tag:
            xpath = f"//{tag}[contains(@id, '{partial_id}')]"
        else:
            xpath = f"//*[contains(@id, '{partial_id}')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element
    except Exception as e:
        print(f'✗ Could not find element with partial ID "{partial_id}" (tag={tag}): {str(e)[:100]}')
        return None


def select_custom_dropdown(driver, dropdown_id, option_text, timeout=DEFAULT_WAIT, description="dropdown"):
    """
    Select from custom ICIMS dropdown (not standard HTML select)
    Clicks the fake dropdown link, then clicks the option
    """
    try:
        wait = WebDriverWait(driver, timeout)
        
        # Find and click the fake dropdown link (the visible clickable element)
        fake_dropdown_id = f"{dropdown_id}_icimsDropdown"
        print(f'Looking for custom dropdown: {fake_dropdown_id}')
        
        fake_dropdown = wait.until(EC.element_to_be_clickable((By.ID, fake_dropdown_id)))
        fake_dropdown.click()
        time.sleep(1)  # Wait for dropdown to open
        
        print(f'✓ Opened custom dropdown')
        
        # Now find and click the option that matches the text
        # Options are in list items with class "dropdown-result"
        results_container_id = f"{dropdown_id}_dropdown-results"
        
        # Wait for results container to be visible
        wait.until(EC.presence_of_element_located((By.ID, results_container_id)))
        
        # Find all options
        options = driver.find_elements(By.XPATH, f"//ul[@id='{results_container_id}']/li[contains(@class, 'dropdown-result')]")
        
        # Click the option that matches our text
        for option in options:
            if option_text.lower() in option.get_attribute('title').lower():
                option.click()
                print(f'✓ Selected "{option.get_attribute("title")}" from {description}')
                time.sleep(0.5)
                return True
        
        print(f'✗ Could not find option "{option_text}" in {description}')
        return False
        
    except Exception as e:
        print(f'✗ Failed to select from custom dropdown {description}: {str(e)[:200]}')
        return False


def move_mouse_to_element(driver, by, value, timeout=DEFAULT_WAIT, description="element"):
    """Move mouse to an element (human-like hover)"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        
        print(f'✓ Moved mouse to {description}')
        time.sleep(random.uniform(0.3, 0.7))  # Random delay after hover
        return True
    except Exception as e:
        print(f'✗ Failed to move mouse to {description}: {str(e)[:100]}')
        return False


def click_with_mouse(driver, by, value, timeout=DEFAULT_WAIT, description="element"):
    """Click element using mouse movement (more human-like)"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        
        # Move to element first, then click
        actions = ActionChains(driver)
        actions.move_to_element(element).pause(random.uniform(0.2, 0.5)).click().perform()
        
        print(f'✓ Clicked {description} with mouse')
        time.sleep(1)
        return True
    except Exception as e:
        print(f'✗ Failed to click {description} with mouse: {str(e)[:100]}')
        return False


def random_mouse_movement(driver):
    """Perform random mouse movements to look more human"""
    try:
        actions = ActionChains(driver)
        
        # Move to random positions
        for _ in range(random.randint(2, 4)):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            actions.move_by_offset(x_offset, y_offset).pause(random.uniform(0.1, 0.3))
        
        actions.perform()
        print('✓ Performed random mouse movements')
        return True
    except Exception as e:
        print(f'✗ Random mouse movement failed: {str(e)[:100]}')
        return False


def scroll_slowly(driver, scroll_amount=300, steps=5):
    """Scroll the page slowly like a human"""
    try:
        scroll_per_step = scroll_amount // steps
        
        for i in range(steps):
            driver.execute_script(f"window.scrollBy(0, {scroll_per_step});")
            time.sleep(random.uniform(0.1, 0.3))
        
        print(f'✓ Scrolled {scroll_amount}px')
        return True
    except Exception as e:
        print(f'✗ Scroll failed: {str(e)[:100]}')
        return False


def human_like_click(driver, by, value, timeout=DEFAULT_WAIT, description="element"):
    """Most human-like click: hover, wait, then click"""
    try:
        # First move mouse to element
        if not move_mouse_to_element(driver, by, value, timeout, description):
            return False
        
        # Random pause before clicking
        time.sleep(random.uniform(0.3, 0.8))
        
        # Click with mouse movement
        return click_with_mouse(driver, by, value, timeout, description)
        
    except Exception as e:
        print(f'✗ Human-like click failed: {str(e)[:100]}')
        return False


def toggle_checkbox(driver, by, value, ensure_checked=True, timeout=DEFAULT_WAIT, description="checkbox"):
    """
    Toggle a checkbox with delays
    If ensure_checked=True, ensures it ends up checked
    If ensure_checked=False, ensures it ends up unchecked
    """
    try:
        wait = WebDriverWait(driver, timeout)
        checkbox = wait.until(EC.presence_of_element_located((by, value)))
        
        # Check current state
        is_checked = checkbox.is_selected()
        print(f'Checkbox "{description}" is currently: {"checked" if is_checked else "unchecked"}')
        
        # If already in desired state, toggle it first then toggle back
        if is_checked == ensure_checked:
            print(f'Toggling {description} off first...')
            time.sleep(2)
            checkbox.click()
            time.sleep(2)
            print(f'Now toggling {description} back on...')
            checkbox.click()
            time.sleep(1)
        else:
            # Just toggle once to reach desired state
            print(f'Toggling {description} to {"checked" if ensure_checked else "unchecked"}...')
            time.sleep(2)
            checkbox.click()
            time.sleep(1)
        
        # Verify final state
        final_state = checkbox.is_selected()
        if final_state == ensure_checked:
            print(f'✓ Checkbox "{description}" is now {"checked" if ensure_checked else "unchecked"}')
            return True
        else:
            print(f'✗ Checkbox "{description}" state verification failed')
            return False
            
    except Exception as e:
        print(f'✗ Failed to toggle {description}: {str(e)[:100]}')
        return False
    

def switch_to_nested_iframes(driver, iframe_chain, timeout=DEFAULT_WAIT):
    """
    Switch to nested iframes one by one.
    iframe_chain: list of iframe IDs or XPaths (outer → inner)
    """
    try:
        switch_to_main_content(driver)
        wait = WebDriverWait(driver, timeout)
        for iframe_id in iframe_chain:
            print(f'→ Switching to iframe: {iframe_id}')
            iframe = wait.until(EC.presence_of_element_located((By.ID, iframe_id)))
            driver.switch_to.frame(iframe)
            time.sleep(1)
        print(f'✓ Switched to nested iframes: {" > ".join(iframe_chain)}')
        return True
    except Exception as e:
        print(f'✗ Failed to switch nested iframes: {str(e)[:100]}')
        return False
