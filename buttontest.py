from playwright.sync_api import sync_playwright
import time

def test_modal_locators():
    with sync_playwright() as p:
        # Launch browser in headed mode for debugging
        browser = p.chromium.launch(headless=False, slow_mo=1000)  # slow_mo adds delay to make actions visible
        page = browser.new_page()
        
        try:
            # Navigate to a job page
            page.goto("https://au.gradconnection.com/employers/ey/jobs/ey-ey-vacationer-computer-science-program-6/")
            page.wait_for_load_state("networkidle")
            
            print("Looking for Apply button...")
            # Try different Apply button selectors
            apply_selectors = [
                "button:has-text('Apply')",
                "button:has-text('APPLY')",
                "button.btn-danger",
                ".jobinformationsection button",
                "//button[contains(text(), 'Apply')]"  # XPath
            ]
            
            apply_button = None
            used_selector = None
            
            for selector in apply_selectors:
                button = page.locator(selector).first  # Use `.first` to target the first button only
                if button.is_visible():
                    print(f"Found visible Apply button with selector: {selector}")
                    print(f"Button text: '{button.text_content()}'")
                    apply_button = button
                    used_selector = selector
                    break
            
            if apply_button:
                print("\nClicking Apply button...")
                apply_button.click()
                
                # Wait for modal to appear or a brief timeout
                time.sleep(2)  # Wait 2 seconds for modal to appear
                
                # Check for modal and login button
                print("\nChecking for modal and login button...")
                
                # Try locating the modal
                print("Modal appeared!")
                
                # Locate and click the login button
                login_button = page.locator("#forcelogin").first
                if login_button.is_visible():
                    print("Found visible Login button.")
                    login_button.click()
                    print("Clicked the Login button.")
                else:
                    print("Login button not found or not visible.")
            
            else:
                print("Could not find Apply button!")
            
            # Wait for manual inspection
            print("\nWaiting 20 seconds for manual inspection...")
            time.sleep(20)
            
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    test_modal_locators()
