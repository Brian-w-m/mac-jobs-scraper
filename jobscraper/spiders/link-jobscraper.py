# Discuss scraping workflow for linkedin cos its complicated

import scrapy
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

class JobSpiderLink(scrapy.Spider):
    name = "jobspider-link"
    cookies = None

    def start_requests(self):
        """Start by navigating to LinkedIn Jobs, logging in, and performing a search."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            try:
                # Go to LinkedIn Login page
                page.goto("https://www.linkedin.com/login")
                page.wait_for_load_state("networkidle")

                # Load credentials from .env file
                load_dotenv()
                username = os.getenv("LINKEDIN_USERNAME")
                password = os.getenv("LINKEDIN_PASSWORD")

                # Log in
                page.fill("#username", username)
                page.fill("#password", password)
                page.click("#organic-div > form > div.login__form_action_container > button")
                
                # Wait for login to complete
                page.wait_for_timeout(5000)

                # Navigate to LinkedIn Jobs page
                page.goto("https://www.linkedin.com/jobs/")
                page.wait_for_timeout(4000)


                # Fill in the search fields
                page.fill('input[aria-label="Search by title, skill, or company"]', "Software engineer intern")
                page.press('input[aria-label="Search by title, skill, or company"]', "Enter")
                # page.fill('input[aria-label="City, state, or zip code"]', "Melbourne")
                # page.press('input[aria-label="City, state, or zip code"]', "Enter")
                page.wait_for_timeout(4000)

                # Scrape the search results page
                search_url = page.url  # Get the URL of the search results page

                # Save cookies for authenticated requests
                self.cookies = page.context.cookies()

                browser.close()

                # Use the search URL to perform the scraping
                yield scrapy.Request(search_url, callback=self.parse, cookies=self.cookies)

            except Exception as e:
                self.logger.error(f"Error during login or search: {e}")
                browser.close()

    def parse(self, response):
        """Parse the search results page."""
        # Extract links to individual job postings
        job_links = response.css("a.job-card-container__link::attr(href)").getall()

        for link in job_links:
            # Follow each job link with the cookies for authentication
            yield response.follow(link, self.parse_job_details, cookies=self.cookies)

    def parse_job_details(self, response):
        """Parse individual job details."""
        job_title = response.css('div.job-view-layout.jobs-details h1::text').get()
        job_description = response.css('#job-details > div > p::text').get()

        yield {
            "job_title": job_title,
            "job_description": job_description,
        }
