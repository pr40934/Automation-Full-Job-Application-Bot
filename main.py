# main.py - Main execution script

from utils.browser_utils import setup_driver
from steps.step1_click_apply import click_apply_button
from steps.step2_enter_email import enter_email
from steps.step3_handle_login import handle_login_page
from steps.step4_enter_password import enter_password
from steps.step5_fill_personal_info import fill_personal_info
from steps.step6_questionnaire import answer_questionnaire
from steps.step7_eeo_form import fill_eeo_form  # ✅ new step added
from steps.step8_job_specific import fill_job_specific_questions
from steps.step9_final_submission import final_submission  # ✅ Step 9
from steps.final_confirmation import final_confirmation  


def run_application():
    """Run the complete job application process"""
    print('=' * 50)
    print('STARTING JOB APPLICATION AUTOMATION')
    print('=' * 50)
    
    driver = setup_driver()
    
    try:
        # Step 1: Click Apply Button
        if not click_apply_button(driver):
            print('\n✗ Application stopped at Step 1')
            return False
        
        # Step 2: Enter Email
        if not enter_email(driver):
            print('\n✗ Application stopped at Step 2')
            return False
        
        # Step 3: Handle login redirect (if it appears)
        if not handle_login_page(driver):
            print('\n✗ Application stopped at Step 3')
            return False
        
        # Step 4: Enter password and login
        if not enter_password(driver):
            print('\n✗ Application stopped at Step 4')
            return False
        
        # https://careers-aeieng.icims.com/jobs/5417/engineering-data-analyst/candidate?from=login&eem=1PcmIdfxyJToZ1TVbBwvUZsAPGIjA0cQGuBk2OjCoqpw41sA8mQEmjuoaV_lHZc_&code=8eccd89019c62ed97782627ad651de88e5bfa6730efe046089239364ae292120
        # Step 5: Fill personal information form
        if not fill_personal_info(driver):
            print('\n✗ Application stopped at Step 5')
            return False
        
        # https://careers-aeieng.icims.com/jobs/5417/engineering-data-analyst/form?form=standard_employment_application_library&step=2&type=1&hashed=851238989
        # Step 6: Answer questionnaire
        if not answer_questionnaire(driver):
            print('\n✗ Application stopped at Step 6')
            return False
        

        # https://careers-aeieng.icims.com/jobs/5417/engineering-data-analyst/eeo?back=
        # Step 7: Fill EEO / Voluntary Information Form
        if not fill_eeo_form(driver):
            print('\n✗ Application stopped at Step 7')
            return False
        
        # https://careers-aeieng.icims.com/jobs/5417/engineering-data-analyst/questions
        # Step 8
        if not fill_job_specific_questions(driver):
            print('\n✗ Application stopped at Step 8')
            return False


        # After Step 8 in run_application():
        if not final_submission(driver):
            print('\n✗ Application stopped at Step 9')
            return False
        
        if not final_confirmation(driver):
            print('\n✗ Stopped at Step 10'); return False
        
        print('=' * 50)
        print('✓ APPLICATION COMPLETED SUCCESSFULLY!')
        print('=' * 50)
        
        # Keep browser open to see the result
        input("Press Enter to close the browser...")
        return True
        
    except Exception as e:
        print('=' * 50)
        print(f'✗ CRITICAL ERROR: {str(e)}')
        print('=' * 50)
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        print('\nClosing browser...')
        driver.quit()
        print('Done!')


if __name__ == "__main__":
    run_application()