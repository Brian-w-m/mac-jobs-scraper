# Install packages in miniconda (base)
# Run scrapy crawl llmjobspider -O outputllm.json
# scrapy shell https://au.gradconnection.com/employers/ey/jobs/ey-ey-vacationer-computer-science-program-6/

import scrapy
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

class LLMJobSpider(scrapy.Spider):
    name = "llmspider"
    start_urls = ["https://au.gradconnection.com/internships/computer-science/australia/"]
    
    # Store cookies here
    cookies = None

    def start_requests(self):
        # Start by logging in to the website
        yield scrapy.Request("https://au.gradconnection.com/login/", callback=self.login)

    def login(self, response):
        """Log in to the website and save the session cookies"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            try:
                # Go to the login page
                page.goto("https://au.gradconnection.com/login/")
                page.wait_for_load_state("networkidle")
                
                # Load credentials from .env file
                load_dotenv()
                username = os.getenv("GRADCONNECTION_USERNAME")
                password = os.getenv("GRADCONNECTION_PASSWORD")
                
                # Fill in login form
                page.fill("#email", username)
                page.fill("#password", password)
                page.click("div.full-row.form-buttons button")
                
                # Wait for navigation after login
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(1000)

                # Save the session cookies
                self.cookies = page.context.cookies()
                browser.close()

                # Continue with the next requests (scraping job postings)
                for url in self.start_urls:
                    yield scrapy.Request(url, callback=self.parse, cookies=self.cookies)
            
            except Exception as e:
                self.logger.error(f"Error during login: {e}")
                browser.close()

    def parse(self, response):
        # Extract links to individual job postings
        job_links = response.css("a.box-header-title::attr(href)").getall()

        for link in job_links:
            # Follow each job link with the cookies for authentication
            yield response.follow(link, self.parse_job_details, cookies=self.cookies)
            
        # Handle pagination (if applicable)
        # next_page = response.css('a.pagination__link--next::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, self.parse, cookies=self.cookies)

    def parse_job_details(self, response):
        # Extract detailed information from each job page
        job_title = response.css('h1.employers-profile-h1::text').get()
        job_description = response.css("div.content-panel-container.right-content-panel.padding-left *::text").getall()
        
        # Get the application link (no need to log in again)
        application_link = self.get_application_link(response.url)

        yield {
            "title": job_title,
            "description": job_description,
            "application_link": application_link
        }

    def get_application_link(self, url):
        """Get the application link after login"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            try:
                # Set cookies for the authenticated session
                page.context.add_cookies(self.cookies)

                # Go to the job page
                page.goto(url)
                page.wait_for_load_state("networkidle")
                
                # Click the Apply button
                apply_button = page.locator("button.btn-danger").first
                if apply_button.is_visible():
                    apply_button.click()
                    
                    page.wait_for_load_state("networkidle")
                
                    pages = page.context.pages

                    if len(pages) > 1:
                        new_tab = pages[-1]  # The new tab should be the last one in the list
                        new_tab.wait_for_load_state("networkidle")  # Ensure the new tab is fully loaded
                        return new_tab.url  # Return the URL of the new tab

                # Return the final URL (application page)
                return page.url
            except Exception as e:
                self.logger.error(f"Error getting application link: {e}")
                return None
            finally:
                browser.close()