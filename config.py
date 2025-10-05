# Job application details
JOB_URL = "https://careers-aeieng.icims.com/jobs/5417/engineering-data-analyst/job"
REDIRECT_URL = "https://careers-aeieng.icims.com/jobs/5417/engineering-data-analyst/candidate?from=login&eem=otA4jR_Ym9vistiCWMd5N-31ML72-vRz8uuyrSTZGlpJFTXqBMH_1rl1UIiBQ4HZ&code=39f1d5b9f549392cee6b3e6a372432c5c9498d20e066b8a5204e6243867cc900"

# User credentials and information
EMAIL = "dafiy70001@bllibl.com"
PASSWORD = "DAfiy70001@bllibl.com"
# EMAIL = "010pratap@gmail.com"
# PASSWORD = "010Pratap@gmail.com"

# Personal information for job application
PERSONAL_INFO = {
    "first_name": "jack",
    "last_name": "daniels",
    "phone_type": "Mobile",  # Options: Mobile, Home, Work
    "phone_number": "6743675488",
    "phone_extension": "+95",
    "address_street": "123 Main St",
    "address_city": "Adhmb",
    "address_zip": "34211",
    "country": "India",
    "state": "Andhra Pradesh"
}

# Questionnaire answers
QUESTIONNAIRE = {
    "work_in_us": "Yes",  # Are you legally authorized to work in the U.S.?
    "need_sponsorship": "Yes",  # Do you require immigration sponsorship?
    "over_18": "Yes",  # Are you at least 18 years old?
    "previously_employed": "No",  # Have you worked for this Company before?
    "relatives_employed": "No",  # Do you have any relatives employed here?
    "signature_agree": True  # Check signature checkbox
}


# Browser settings
BROWSER_OPTIONS = {
    "start_maximized": True,
    "headless": False,  # Set to True to run without opening browser window
    "disable_automation": True,
    "add_human_delays": True  # Add random delays to look more human
}

# EEO / Voluntary Information
EEO_INFO = {
    "gender": "Male",
    "race": "Asian (Not Hispanic or Latino)",
    "disability": "No",
    "veteran": "No"
}

# Job specific questions answers
JOB_SPECIFIC = {
    "source": "LinkedIn",  # How did you hear about this position?
    "source_other": "",     # If Other, please specify
    "work_auth": "H1B"     # What allows you to work in the U.S.?
}


# Wait timeouts (in seconds)
DEFAULT_WAIT = 20
SHORT_WAIT = 5
LONG_WAIT = 30

# Human-like typing delay (in seconds)
TYPING_DELAY = 0.1  # Delay between each keystroke


# iframe identifiers
IFRAME_ID = "icims_content_iframe"
FORM_IFRAME_ID = "icims_formFrame"  # For questionnaire page

RESUME_PATH = r"C:\Users\admin\Desktop\Projects\SquirrelView\fakeResum.pdf"


