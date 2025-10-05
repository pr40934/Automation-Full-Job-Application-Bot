# steps/__init__.py

"""
Steps package - Contains all automation steps for job application
"""

from .step1_click_apply import click_apply_button
from .step2_enter_email import enter_email
from .step3_handle_login import handle_login_page, wait_for_url_change, check_for_login_redirect
from .step4_enter_password import enter_password, check_for_password_page
# Add more imports as you create new steps
# from .step5_xxx import step5_function
# from .step6_xxx import step6_function

__all__ = [
    'click_apply_button',
    'enter_email',
    'handle_login_page',
    'wait_for_url_change',
    'check_for_login_redirect',
    'enter_password',
    'check_for_password_page',
    # Add more function names here
]