# Install packages in miniconda (base)
# Run scrapy crawl jobspider -O output.json

import scrapy
import os
from groq import Groq
from dotenv import load_dotenv

class JobSpider(scrapy.Spider):
    name = "jobspider"
    start_urls = ["https://au.gradconnection.com/internships/computer-science/australia/"]

    def parse(self, response):
        # Extract links to individual job postings
        job_links = response.css("a.box-header-title::attr(href)").getall()

        for link in job_links:
            # Follow each job link
            yield response.follow(link, self.parse_job_details)

    def parse_job_details(self, response):
        # Extract job details from the job page
        job_title = response.css('h1.employers-profile-h1::text').get()
        job_description = response.css('div.campaign-content-container p::text').getall()
        job_type = response.css('#app > span > div.dashboard-site-container.grey-bg > main > section.grey-bg > div.grid-container > div > div.sides-content-container > div > div.content-panel-container.right-content-panel.padding-left > div.jobinformationsection.landing-side-panel-container > ul > li:nth-child(1)::text').get()
        discipline = response.css('#app > span > div.dashboard-site-container.grey-bg > main > section.grey-bg > div.grid-container > div > div.sides-content-container > div > div.content-panel-container.right-content-panel.padding-left > div.jobinformationsection.landing-side-panel-container > ul > li:nth-child(2) > div > div::text').get()
        work_rights = response.css('#app > span > div.dashboard-site-container.grey-bg > main > section.grey-bg > div.grid-container > div > div.sides-content-container > div > div.content-panel-container.right-content-panel.padding-left > div.jobinformationsection.landing-side-panel-container > ul > li:nth-child(3) > div > div::text').get()
        work_from_home = response.css('#app > span > div.dashboard-site-container.grey-bg > main > section.grey-bg > div.grid-container > div > div.sides-content-container > div > div.content-panel-container.right-content-panel.padding-left > div.jobinformationsection.landing-side-panel-container > ul > li:nth-child(4) > span::text').get()
        location = response.css('#app > span > div.dashboard-site-container.grey-bg > main > section.grey-bg > div.grid-container > div > div.sides-content-container > div > div.content-panel-container.right-content-panel.padding-left > div.jobinformationsection.landing-side-panel-container > ul > li:nth-child(5) > span > div > div::text').getall()
        start_date = response.css('#app > span > div.dashboard-site-container.grey-bg > main > section.grey-bg > div.grid-container > div > div.sides-content-container > div > div.content-panel-container.right-content-panel.padding-left > div.jobinformationsection.landing-side-panel-container > ul > div > li > p::text').getall()
        closing_date = response.css('#app > span > div.dashboard-site-container.grey-bg > main > section.grey-bg > div.grid-container > div > div.sides-content-container > div > div.content-panel-container.right-content-panel.padding-left > div.jobinformationsection.landing-side-panel-container > ul > li:nth-child(7)::text').getall()


        load_dotenv()
        client = Groq(
            api_key=os.getenv("groq_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Here is the job description: {job_description}. Provide a summary. Do not add any extra text telling me the summary is below.",
            }],
            model="Llama3-8b-8192",
        )

        # Get the cleaned and summarized job information
        job_summary = chat_completion.choices[0].message.content

        yield {
            "job_title": job_title,
            "job_description": job_summary,
            "job_type": job_type,
            "discipline": discipline,
            "work_rights": work_rights,
            "work_from_home": work_from_home,
            "location": location,
            "start_date": start_date,
            "closing_date": closing_date
        }
