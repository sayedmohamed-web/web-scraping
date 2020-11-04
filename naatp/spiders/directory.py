# -*- coding: utf-8 -*-
import scrapy


class DirectorySpider(scrapy.Spider):
    name = 'directory'
    start_urls = ['https://www.naatp.org/resources/addiction-industry-directory/']

    def parse(self, response):
        urls = response.css(
            'table.views-table td.views-field-display-name a::attr(href)'
            ).getall()

        for url in urls:
            yield response.follow(url=url, callback=self.parse_details)
        
        for href in response.css('li.pager-next a::attr(href)'):
            yield response.follow(url=href, callback=self.parse)
    
    def parse_details(self, response):
        yield {
            'name': response.css('h1::text').get(),
            'accredited': response.css('h1 span.accredited-Yes::text').get(),
            'mailing address': response.css('div.views-field-postal-code span.field-content::text').get(),
            'phone': response.css('div.views-field-phone span.field-content::text').get(),
            'email': response.css('div.views-field-email span.field-content a::attr(href)').get(),
            'website': response.css('div.views-field-url span.field-content a::attr(href)').get(),
            'Facility of': response.css('div.views-field-display-name-1 span.field-content a::attr(href)').get(''),
            'CEO': response.css('div.views-field-ceo-77 span.field-content::text').get(''),
            'CEO Email': response.css('div.views-field-ceo-email-80 span.field-content a::attr(href)').get(''),
            'CEO Phone': response.css('div.views-field-ceo-phone-78 span.field-content::text').get(''),
            'Admissions': response.css('div.views-field-admissions-contact-69 span.field-content::text').get(''),
            'Admissions Email': response.css('div.views-field-admissions-email-72 span.field-content a::attr(href)').get(''),
            'Admissions Phone': response.css('div.views-field-admissions-phone-70 span.field-content::text').get(''),
            'Marketing Contact': response.css('div.views-field-marketing-contact-73 span.field-content::text').get(''),
            'Marketing Email': response.css('div.views-field-marketing-email-76 span.field-content a::attr(href)').get(''),
            'Marketing Phone': response.css('div.views-field-marketing-phone-74 span.field-content::text').get(''),
            'Membership Type': response.css('div.views-field-membership-type span.field-content::text').get(''),
            'About The Organization': ''.join(text for text in response.css('div.views-field-organization-description-11 span.field-content p::text').getall()),
            'Mission Statement': response.css('div.views-field-mission-statement-21 span.field-content p::text').get(''),
            'Licensing Body': response.css('div.views-field-licensing-body-32 span.field-content p::text').get(''),
            'Accreditation': response.css('div.views-field-accreditation-35 span.field-content::text').get(''),
            'Year Founded': response.css('div.views-field-year-founded-22 span.field-content::text').get(''),
            'Language Services': response.css('div.views-field-bilingual-services-14 span.field-content::text').get(''),
            'Level of Treatment Care': response.css('div.views-field-levels-of-treatment-care-25 span.field-content::text').get(''),
            'Specialty Programs': response.css('div.views-field-specialty-programs-30 span.field-content::text').get(''),
            'Length of Stay': response.css('div.views-field-length-of-stay-26 span.field-content::text').get(''),
            'Number of Beds': response.css('div.views-field-number-of-beds-23 span.field-content::text').get(''),
            'Payment Assistance Available': response.css('div.views-field-payment-assistance-available-28 span.field-content::text').get(''),
            'Licensed': response.css('div.views-field-licensed-31 span.field-content::text').get('') 
        }
