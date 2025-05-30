import os
import random
from time import sleep
import pytest
import undetected_chromedriver as uc
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = uc.Chrome(options=options, version_main=136)
    driver.get('https://israelpost.co.il/')
    sleep(4)
    yield driver
    driver.quit()

def test_tc03(driver):
    '''Login with invalid password'''

    username = "mohammadar03@gmail.com"
    password = "invalid_password"

    wait = WebDriverWait(driver, 10)

    # Wait and click login button
    login_page = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')))
    login_page.click()

    # Wait for the username field and enter it
    username_field = wait.until(EC.visibility_of_element_located((By.ID, 'UserID')))
    username_field.send_keys(username)

    # Wait for the password field and enter it
    password_field = wait.until(EC.visibility_of_element_located((By.ID, 'Password')))
    password_field.send_keys(password)

    # Wait and click the login button

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
    login_btn.click()

    # Wait for error message
    error_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "field-validation-error"))
    )
    error_text = error_element.text.strip()

    assert error_text == "אחד או יותר מנתוני ההזדהות שהזנת אינם תקינים"

def test_tc04(driver):
    wait = WebDriverWait(driver, 10)

    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(3)

    username = driver.find_element(By.ID, 'UserID')
    username.send_keys('')

    password = driver.find_element(By.ID, 'Password')
    password.send_keys('')

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
    login_btn.click()

    sleep(3)
    user_error = driver.find_element(By.ID,'UserID-error')
    assert user_error.text == 'חובה להזין מספר ת.ז או מייל', 'Error'

    pass_error = driver.find_element(By.ID,'Password-error')
    assert pass_error.text == 'חובה להזין סיסמא', 'Error'

    sleep(2)
#

def test_tc05(driver):

    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(3)

    password = driver.find_element(By.ID, 'Password')
    password.send_keys('jmwgonqrj')

    driver.execute_script("document.body.style.zoom='80%'")

    input_type = password.get_attribute('type')

    assert input_type == 'password',"Password field is not masked"

    sleep(3)

def test_tc06(driver):

    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    driver.execute_script("document.body.style.zoom='80%'")

    sleep(3)

    forgot_password = driver.find_element(By.ID,'btnShowForgotpwd')
    forgot_password.click()

    sleep(3)

    signup_title = driver.find_element(By.ID,'step1title')
    assert signup_title.text == 'שכחתי סיסמה','Failed to redirect to sign up form'

    sleep(2)



def test_tc08(driver):

    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    driver.execute_script("document.body.style.zoom='80%'")

    sleep(3)

    signup_btn = driver.find_element(By.ID,'gotoRegister')
    signup_btn.click()

    sleep(2)

    signup_title = driver.find_element(By.XPATH,'//div[text()="הרשמה"]')
    assert signup_title.text == 'הרשמה', "Failed to move to sign up form"

    sleep(2)

@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skipping Google Sign-In test in CI environment")
def test_tc10(driver):
    wait = WebDriverWait(driver, 10)

    # Click login
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="כניסה לאיזור אישי"]')))
    login_btn.click()
    sleep(2)

    # Store current window
    original_window = driver.current_window_handle
    #
    # # Click Google login
    gmail_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="התחברות דרך גוגל"]')))
    gmail_btn.click()
    #
    # # Wait for new window
    wait.until(EC.number_of_windows_to_be(2))
    #
    # # Switch to new window
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break
    #
    # # Now continue with Gmail login
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="email"]')))
    email_input.send_keys('Ahmad060590@gmail.com')

    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]/..')))
    next_btn.click()
    sleep(2)

    password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    password_input.send_keys('Ahmad123*')
    #
    # # Wait for element to be visible and clickable
    next2_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="passwordNext"]/div/button')))
    driver.execute_script("arguments[0].click();", next2_btn)  # Bypass click intercept

    sleep(6)

    # # Switch back to the original window
    driver.switch_to.window(original_window)

    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div[1]/div/div/div/div[3]/div[3]/div[3]/a[1]')))

    # Assert that the user is logged in
    logged_in_text = driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div/div/div[3]/div[3]/div[3]/a[1]').text
    assert "שלום" in logged_in_text, "User is not logged in"


def test_tc13(driver):
    '''Try to sign up with empty fields '''
    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('')
    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)

    error_message_elements = []
    for i in range(1, 6):
        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[{i}]/label[2]"
        error_message_elements.append(driver.find_element(By.XPATH, xpath))

    expected_messages = [
        'חובה להזין שם פרטי',
        'חובה להזין שם משפחה',
        'חובה להזין כתובת מייל',
        "חובה להזין מס' טלפון נייד",
        'חובה להזין סיסמה'
    ]
    assert len(error_message_elements) == len(
        expected_messages), f"Expected {len(expected_messages)} error messages but found {len(error_message_elements)}"

    for i, expected_text in enumerate(expected_messages):
        actual_text = error_message_elements[i].text
        assert actual_text == expected_text, f"Error mismatch at {i}: expected '{expected_text}', got '{actual_text}'"


def test_tc14(driver):
    '''Check if first name field will accept spaces
Valid phone number email family name and password
1 open sign up page
2 write a first name with a space in it
4 fill in the rest of the fields correctly
3 press the open an account button
Should allow it and show no errors

'''
    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('test test')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('Test1234')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)
    # Check for error message
    # Locate the error message element dynamically
    #        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    # should apear no error message
    error_message_element = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    )
    # Check if the error message element is empty
    assert len(error_message_element) == 0, "Error message should not be displayed"


def test_tc15(driver):
    '''Check if the first name field allows different languages
Valid phone number email family name and password
1 open sign up page
2 fill in the first name field a name with a different language
3 enter the rest of the filed correctly
4 press the open an account button
Should be able to register with any name in any language
Only accepts english and hebrew letter other than that will show an error
“Please only enter letters in this field “

'''
    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('محمد')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('Test1234')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)

    # Check for error message
    # Locate the error message element dynamically
    #        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    # should apear an error message
    error_message_element = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    )

    print(len(error_message_element))
    # Check if the error message element is empty
    assert len(error_message_element) > 0, "Error message should be displayed"

    msg = 'ניתן להזין אותיות בלבד'
    assert error_message_element[
               0].text == msg, f"Expected error message '{msg}', but got '{error_message_element[0].text}'"


def test_tc16(driver):
    '''TC-16
Check if the first name field will reject numbers
Valid phone number email family name and password
1 open sign up page
2 fill in the first name field a name with one number at least
3 enter the rest of the filed correctly
4 press the open an account button
Will show an error that says that you can't use numbers in this field

'''
    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('mohammed123')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('Test1234')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)

    # Check for error message
    # Locate the error message element dynamically
    #        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    # should apear an error message
    error_message_element = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    )
    print(len(error_message_element))
    # Check if the error message element is empty
    assert len(error_message_element) > 0, "Error message should be displayed"

    msg = 'ניתן להזין אותיות בלבד'
    assert error_message_element[
               0].text == msg, f"Expected error message '{msg}', but got '{error_message_element[0].text}'"


def test_tc17(driver):
    '''TC- 17
Check if the first name field will reject special characters
Valid phone number email family name and password
1 open sign up page
2 fill in the first name field a name with one  special character at least language
3 enter the rest of the filed correctly
4 press the open an account button
Will show an error that says that you can't use numbers in this field
Shows and error “Please only enter letters in this field

'''

    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('mohammed!@@')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('Test1234')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)

    # Check for error message
    # Locate the error message element dynamically
    #        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    # should apear an error message
    error_message_element = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    )
    print(len(error_message_element))
    # Check if the error message element is empty
    assert len(error_message_element) > 0, "Error message should be displayed"

    msg = 'ניתן להזין אותיות בלבד'
    assert error_message_element[
               0].text == msg, f"Expected error message '{msg}', but got '{error_message_element[0].text}'"


def test_tc18(driver):
    '''TC-18
    Check if the first name field will accept single character names
    Valid phone number email family name and password
    1 open sign up page
    2 fill in the first name field a name with one  character
    3 enter the rest of the filed correctly
    4 press the open an account button
    Will have no errors
    No errors
    pass

    '''
    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('M')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('Test1234')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)
    # Check for error message
    # Locate the error message element dynamically
    #        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    # should apear no error message
    error_message_element = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    )
    # Check if the error message element is empty
    assert len(error_message_element) == 0, "Error message should not be displayed"


def test_tc19(driver):
    '''TC-19
Fill the first name field with Hyphenated names for example (Ben-David)
Valid phone number email family name and password
1 open sign up page
2 fill in the first name field with a hyphenate name
3 enter the rest of the filed correctly
4press the open an account button
No errors expected
No errors
pass

'''

    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('Mohammed-Ben')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('Test1234')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)
    # Check for error message
    # Locate the error message element dynamically
    #        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    # should apear no error message
    error_message_element = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    )
    # Check if the error message element is empty
    assert len(error_message_element) == 0, "Error message should not be displayed"


def test_tc20(driver):
    '''TC-20
Check if the name field will trail spaces
Valid phone number email
Name
family name and password
1 open sign up page
2 before writing the name enter multiple spaces
3 enter the rest of the filed correctly
4 press the open an account button
The website need to delete the extra spaces for example
“    basel”
Should become “basel”
Automatically
Does not trail spaces

'''
    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('    mhmd')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('Test1234')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)

    # get the value of the name field
    name_value = driver.find_element(By.XPATH,
                                     "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input").get_attribute(
        'value')
    # Check if the name value is equal to 'mhmd'
    assert name_value == 'mhmd', f"Expected name value to be 'mhmd', but got '{name_value}'"

"""

# def test_tc22(driver):
#
#     sign_up_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
#     sign_up_page.click()
#
#     sign_up_page_2 = driver.find_element(By.ID,'gotoRegister')
#     driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_page_2)
#     sign_up_page_2.click()
#     sleep(3)
#
#
#     username = driver.find_element(By.ID, 'FirstNameRegister')
#     username.send_keys('moha+adf')
#
#     sleep(3)
#     sign_up_page_3 = driver.find_element(By.ID, 'Surname')
#     sign_up_page_3.click()
#     first_name_error = driver.find_element(By.ID, 'FirstNameRegister-error')
#     assert first_name_error.text == 'ניתן להזין אותיות בלבד', 'Error'

"""
def test_tc27(driver):
    sign_up_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    sign_up_page.click()

    sleep(1)
    sign_up_page_2 = driver.find_element(By.ID, 'gotoRegister')
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_page_2)
    sign_up_page_2.click()

    sleep(3)

    mobile = driver.find_element(By.ID, 'Mobile')
    mobile.send_keys('+972584595')

    sleep(1)
    surname = driver.find_element(By.ID, 'Surname')
    surname.click()

    sleep(2)
    mobile_error = driver.find_element(By.ID, 'Mobile-error')

    assert mobile_error.text == 'חובה להזין ספרות בלבד', 'Error: Expected validation message not found'

def test_tc28(driver):

    sign_up_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    sign_up_page.click()

    sleep(1)
    sign_up_page_2 = driver.find_element(By.ID, 'gotoRegister')
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_page_2)
    sign_up_page_2.click()

    sleep(3)

    mobile = driver.find_element(By.ID, 'Mobile')
    mobile.send_keys('test')

    sleep(1)
    surname = driver.find_element(By.ID, 'Surname')
    surname.click()

    sleep(2)
    mobile_error = driver.find_element(By.ID, 'Mobile-error')

    assert mobile_error.text == 'Please enter a value greater than or equal to 10.', 'Error: Expected validation message not found'


def test_tc34(driver):
    '''TC-34
Check if the common password are rejected
N/A
1 open the sign up page
2 fill in the password field a very common password like Password123
3 click the sign up button
The website should give a error not to use a very common password
The website does not reject common passwords

'''
    login_page = driver.find_element(By.CLASS_NAME, 'main-login-button.to-login-area.userAnonymous')
    login_page.click()

    sleep(1)

    # Click on sign up button /html/body/div[2]/div[1]/div[5]/div[6]/button
    sign_up_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[6]/button")
    driver.execute_script("arguments[0].scrollIntoView(true);", sign_up_btn)
    sign_up_btn.click()
    sleep(1)

    # name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input
    # family name /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input
    # email /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input
    # phone /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input
    # password /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input

    # populate fields with empty values
    name = driver.find_element(By.XPATH,
                               "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[1]/input")
    name.send_keys('mhmd')

    family_name = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[2]/input")
    family_name.send_keys('test')

    email = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[3]/input")
    email.send_keys('test@test.com')

    phone = driver.find_element(By.XPATH,
                                "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[4]/input")
    phone.send_keys('0501234567')

    password = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div[5]/input")
    password.send_keys('qwerty123')

    sleep(1)

    # sign up button /html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button
    sign_up_btn = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[2]/div[5]/button")
    # Used JavaScript Click to bypasses any UI interference.
    driver.execute_script("arguments[0].click();", sign_up_btn)
    # sign_up_btn.click()
    sleep(1)
    # Check for error message

    # Locate the error message element dynamically
    #        xpath = f"/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    # should apear an error message
    error_message_element = driver.find_elements(
        By.XPATH, "/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/form/div[7]/div[1]/div/label[2]"
    )
    print(len(error_message_element))
    # Check if the error message element is empty
    assert len(error_message_element) > 0, "Error message should be displayed"


def test_tc40(driver):

    menu_btn = driver.find_element(By.CLASS_NAME, 'menu-hamburger-text.menu-hamburger-open.buttonnobordernobkg')
    menu_btn.click()

    sleep(3)

    menu_items = driver.find_element(By.CLASS_NAME,'main-menu-list')
    assert menu_items.is_displayed(),"Menu button is not functional"


def test_tc41(driver):

    post_icon = driver.find_element(By.XPATH, '//img[@alt="דואר ישראל מחברים עולמות בשבילך - לוגו - מעבר לדף הבית"]')
    post_icon.click()

    sleep(3)

    homepage = driver.find_element(By.CLASS_NAME,'carousel-inner')
    assert homepage.is_displayed(),"post icon is not functional"

def test_tc42(driver):

    language_dropdown = driver.find_element(By.XPATH, '//span[text()="עברית"]')
    language_dropdown.click()

    sleep(3)

    dropdown_list = driver.find_element(By.XPATH,'//div[@class="change-culture L active"]')
    assert dropdown_list.is_displayed(),"Language drop down is not functional"

def test_tc43(driver):

    language_dropdown = driver.find_element(By.XPATH, '//span[text()="עברית"]')
    language_dropdown.click()

    sleep(3)

    arabic_btn = driver.find_element(By.XPATH,'//a[text()="العربية"]')
    arabic_btn.click()

    sleep(2)

    menu_in_arabic = driver.find_element(By.XPATH,'//button[text()="قائمة"]')
    assert menu_in_arabic.text == 'قائمة', "The page couldn't redirect to the arabic homepage"

def test_tc44(driver):

    language_dropdown = driver.find_element(By.XPATH, '//span[text()="עברית"]')
    language_dropdown.click()

    sleep(3)

    english_btn = driver.find_element(By.XPATH,'//a[text()="English"]')
    english_btn.click()

    sleep(2)

    menu_in_english = driver.find_element(By.XPATH,'//a[text()="Track and Trace"]')
    assert menu_in_english.text == 'Track and Trace', "The page couldn't redirect to the English homepage"

def test_tc45(driver):

    tenders_btn = driver.find_element(By.XPATH, '//span[text()="סוכני דואר/ זכיינים"]')
    tenders_btn.click()

    # Switch to new tab
    new_tab_handle = driver.window_handles[-1]  # Get the latest opened tab
    driver.switch_to.window(new_tab_handle)

    wait = WebDriverWait(driver, 10)
    tenders_page_2 = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="סוכני דואר / זכיינים"]')))
    sleep(4)
    assert tenders_page_2.text == 'סוכני דואר / זכיינים', "Error"

def test_tc46(driver):

    jobs_btn = driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div/div/div[3]/div[1]/a[2]/img')
    jobs_btn.click()

    sleep(3)
    # Switch to new tab
    new_tab_handle = driver.window_handles[-1]  # Get the latest opened tab
    driver.switch_to.window(new_tab_handle)

    wait = WebDriverWait(driver, 10)
    jobs_title = wait.until(EC.presence_of_element_located((By.XPATH, '//h1[text()="דרושים"]')))
    sleep(4)
    assert jobs_title.text == 'דרושים', "Error"


def test_tc47(driver):

    personal_btn = driver.find_element(By.XPATH, '//a[text()="כניסה לאיזור אישי"]')
    personal_btn.click()

    sleep(3)

    login_title = driver.find_element(By.XPATH,'//div[text()="התחברות"]')
    sleep(3)
    assert login_title.text == 'התחברות',"Personal page button is not working!!"

    sleep(3)

def test_tc48(driver):
    search_page_btn = driver.find_element(By.CSS_SELECTOR, '.site-search-icon.L')

    search_page_btn.click()

    sleep(3)

    search_title = driver.find_element(By.XPATH, '//div[text()="איתור מידע"]')

    sleep(4)
    assert search_title.text == 'איתור מידע', "Error"


def test_tc49(driver):

    get_in_contact_btn = driver.find_element(By.XPATH, '//p[text()="יצירת קשר"]')
    get_in_contact_btn.click()

    sleep(3)

    # Switch to new tab
    new_tab_handle = driver.window_handles[-1]  # Get the latest opened tab
    driver.switch_to.window(new_tab_handle)

    wait = WebDriverWait(driver, 10)
    contact_title = wait.until(EC.presence_of_element_located((By.XPATH,'//h1[@class="form-title"]')))
    sleep(3)
    assert contact_title.text == 'צור קשר | שירות לקוחות דואר ישראל',"Get in contact button is not working!!"


def test_tc50(driver):

    menu_btn = driver.find_element(By.XPATH, '//img[@class="menu-hamburger menu-hamburger-open"]')
    menu_btn.click()
    sleep(3)
    country_post = driver.find_element(By.XPATH,'//a[@class="hidden-mobile dropdown-toggle"]')
    actions = ActionChains(driver)
    actions.move_to_element(country_post).perform()
    sleep(3)
    country_post_submenu = driver.find_element(By.XPATH,'//div[@class="sub-menu-list-bg active"]')
    sleep(1)
    assert country_post_submenu.is_displayed(),"Country post sub menu is not working!!"
    sleep(3)


def test_tc51(driver):

    menu_btn = driver.find_element(By.XPATH, '//img[@class="menu-hamburger menu-hamburger-open"]')
    menu_btn.click()
    sleep(3)
    country_post = driver.find_element(By.XPATH,'//a[@class="hidden-mobile dropdown-toggle"]')
    actions = ActionChains(driver)
    actions.move_to_element(country_post).perform()
    sleep(3)
    digital_letter_btn = driver.find_element(By.XPATH,'//a[text()="מכתב דיגיטלי (רשום ברשת)"]')
    digital_letter_btn.click()
    sleep(2)
    login_title = driver.find_element(By.XPATH,'//div[text()="התחברות"]')
    sleep(3)
    assert login_title.text == 'התחברות',"digital letter button is not working!!"


def test_tc53(driver):

    menu_btn = driver.find_element(By.XPATH, '//img[@class="menu-hamburger menu-hamburger-open"]')
    menu_btn.click()
    sleep(3)
    country_post = driver.find_element(By.XPATH,'//a[@class="hidden-mobile dropdown-toggle"]')
    actions = ActionChains(driver)
    actions.move_to_element(country_post).perform()
    sleep(3)
    registered_mail_btn = driver.find_element(By.XPATH,'/html/body/header/div[1]/nav/div[1]/div/div[3]/div[1]/ul[1]/li[3]/a')
    registered_mail_btn.click()
    sleep(3)
    registered_mail_page = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/h1')
    sleep(3)
    assert registered_mail_page.text == 'משלוח דואר רשום בארץ',"registered mail button is not working!!"


