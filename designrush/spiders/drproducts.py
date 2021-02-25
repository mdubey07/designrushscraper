import scrapy


class DrproductsSpider(scrapy.Spider):
    name = 'drproducts'
    allowed_domains = ['designrush.com']
    start_urls = ['https://www.designrush.com/agency/search-engine-optimization?page=',
                  'https://www.designrush.com/agency/digital-marketing?page=',
                  'https://www.designrush.com/agency/paid-media-pay-per-click?page=']

    # page_number = 1

    def start_requests(self):
        for page_number in range(1, 115):
            yield scrapy.Request(url=self.start_urls[1] + str(page_number), callback=self.parse)

    def parse(self, response):
        for agency in response.css("ul.agency-list li.agency-list-item"):
            agency_url = agency.css("a.js--agency-profile-link::attr(href)").get()
            agency_contact = agency.css("div.agency-list-contact-box a::attr(title)").extract()
            if agency_contact:
                agency_phone = agency_contact[0]
                agency_email = agency_contact[1]

            # agency_email = agency.xpath('//div[@class="agency-list-contact-box"]/a[2]/@title').extract()

            yield scrapy.Request(url=agency_url, callback=self.parse_details, meta={'email': agency_email})

    def parse_details(self, response):
        agency_header = response.css("div.profile-header--data")
        agency_name = agency_header.css("div.profile-header--head h1 a::text").get()
        website_url = agency_header.css("div.profile-header--head h1 a::attr(href)").get()
        review_count = agency_header.css("div.profile-header--reviews span.review-count::text").get()
        if review_count:
            review_count = review_count.split()[0].replace("(", "").strip()
        else:
            review_count = "NA"
        review_rating = agency_header.css("div.profile-header--reviews span.review-rating::text").get()
        if review_rating:
            review_rating = self.rm_whilespace(review_rating)
        else:
            review_rating = "NA"
        slogan = agency_header.css("p.profile-header--slogan::text").get()
        if slogan:
            slogan = slogan.strip()
        else:
            slogan = "NA"
        address = agency_header.xpath('//*[@class="profile-header--address"]/div/span/text()').get()
        # agency_email = response.css("div.contact-data a.agency-mail>span::text").get()
        # agency_email = response.xpath('//a[@class="agency-mail"]/span').get()

        agency_phone = response.css("div.contact-data div.profile-header--address a.agency-phone span::text").get()
        additional_info = response.css("div.tab-overview--additional div.overview-adds--text::text").extract()
        employees = additional_info[0]
        budget = additional_info[1]
        hourly_rate = additional_info[2]
        founded = additional_info[3]

        # description = response.css("div.tab-overview--description::text").extract()
        description = response.xpath(
            '//div[contains(@class, "tab-overview--description")]/descendant-or-self::*/text()').extract()
        if description:
            description = self.rm_whilespace(description)
        services = response.css("ul.services li div.tab-service--title::text").extract()
        if services:
            services = self.rm_whitespace2(services)

        social_links = response.css("div.overview-socials a::attr(href)").extract()
        if social_links:
            social_links = self.rm_whitespace2(social_links)

        team_members = response.xpath('//ul[contains(@class, "team-bio-list")]/li')
        members_list = []
        for team in team_members:
            name = team.xpath('.//div[contains(@class, "tab-teambio--member-name")]/text()').get()
            name = name.strip()
            designation = team.xpath('.//div[contains(@class, "tab-teambio--title")]/text()').get()
            designation = designation.strip()
            temp = name + "-" + designation
            members_list.append(temp)
        if members_list:
            members_list = self.rm_whitespace2(members_list)
        else:
            members_list = "NA"

        yield {
            'Agency Name': agency_name.strip(),
            'Slogan': slogan,
            'url': website_url,
            'address': address,
            'agency email': response.meta.get("email"),
            'agency phone': agency_phone,
            'Agency Members': members_list,
            'reviews': review_count,
            'rating': review_rating,
            'employees': employees,
            'budget': budget,
            'hourly rate': hourly_rate,
            'founded': founded,
            'description': description,
            'services': services,
            'social links': social_links,
        }

    @staticmethod
    def rm_whilespace(query_term):
        if query_term:
            None_ = [nn_.replace('\n', '') for nn_ in query_term]
            None_ = [nn_.strip() for nn_ in None_]
            None_ = filter(None, None_)
            None_ = ' '.join(None_)
            ret_value = None_
            return ret_value
        return query_term

    @staticmethod
    def rm_whitespace2(query_term):
        if query_term:
            None_ = [nn_.replace('\n', '') for nn_ in query_term]
            None_ = [nn_.strip() for nn_ in None_]
            None_ = filter(None, None_)
            None_ = ', '.join(None_)
            ret_value = None_
            return ret_value
        return query_term
