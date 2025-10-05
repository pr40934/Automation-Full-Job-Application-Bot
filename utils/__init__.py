# utils/__init__.py

"""
Utils package - Contains all utility functions for browser automation
"""

from .browser_utils import (
    setup_driver,
    switch_to_iframe,
    switch_to_main_content,
    wait_for_page_load,
    click_element,
    input_text,
    move_mouse_to_element,
    click_with_mouse,
    random_mouse_movement,
    scroll_slowly,
    human_like_click,
    clear_and_input_text,
    select_dropdown_by_text,
    select_dropdown_by_partial_text,
    find_element_by_partial_id,
    select_custom_dropdown,
    toggle_checkbox
)

__all__ = [
    'setup_driver',
    'switch_to_iframe',
    'switch_to_main_content',
    'wait_for_page_load',
    'click_element',
    'input_text',
    'move_mouse_to_element',
    'click_with_mouse',
    'random_mouse_movement',
    'scroll_slowly',
    'human_like_click',
    'clear_and_input_text',
    'select_dropdown_by_text',
    'select_dropdown_by_partial_text',
    'find_element_by_partial_id',
    'select_custom_dropdown',
    'toggle_checkbox'
]