import scrapy
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

class JobSpiderLink(scrapy.Spider):
    name = "jobspider-link"
    start_urls = ["https://www.linkedin.com/jobs/search/?currentJobId=4076504898&f_E=1&geoId=101452733&keywords=Software%20engineer%20intern&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"]

    # Store cookies here
    cookies = None

    def start_requests(self):
        # Start by loggin in to the website
        yield scrapy.Request("https://www.linkedin.com/login", callback=self.login)

    def login(self, response):
        """Log in to the website and save the session cookies"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            try:
                # Go to the login page
                page.goto("https://www.linkedin.com/login")
                page.wait_for_load_state("networkidle")
                
                # Load credentials from .env file
                load_dotenv()
                username = os.getenv("LINKEDIN_USERNAME")
                password = os.getenv("LINKEDIN_PASSWORD")

                # Fill in login form
                page.fill("#username", username)
                page.fill("#password", password)
                page.click("#organic-div button")

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
        job_links = response.css("#ember204::attr(href)").getall()

        for link in job_links:
            # Follow each job link with the cookies for authentication
            yield response.follow(link, self.parse_job_details, cookies=self.cookies)

        # Handle pagination (if applicable)
        # next_page = response.css('a.pagination__link--next::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, self.parse, cookies=self.cookies)

    def parse_job_details(self, response):
        # Extract job details from the job page
        job_title = response.css('temporary').get()
        job_description = response.css('temporary').getall()

        # Get the application link (no need to log in again)
        application_link = self.get_application_link(response.url)

        yield {
            "job_title": job_title,
            "job_description": job_description
        }

    def get_application_link(self, url):
        pass