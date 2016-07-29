# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html
#

def parse_page(url):
    #Read in page
    html = scraperwiki.scrape(url)
    response = lxml.html.fromstring(html)
    
    #Extract elements
    college_name = response.xpath('//*[@class="page-title"]/text()')[0]
    college_url = response.xpath('//*[@class="mem-contact"]/p[2]//a/@href')[0]
    college_address = response.xpath('//*[@class="mem-contact"]/p[1]/text()[1]')[0]
    college_city = response.xpath('//*[@class="mem-contact"]/p[1]/text()[2]')[0]
    college_postalcode = response.xpath('//*[@class="mem-contact"]/p[1]/text()[3]')[0]
    
    print "Successfully scraped %s in %s" % (college_name, college_city)
    
    college_nrcampuses = response.xpath('//*[@class="mem-stats"]/div[1]/h2/text()')
    print "Found %s campuses" % college_nrcampuses
    
    college_stats = response.xpath('//*[@class="mem-stats"]/div[2]/ul//li')
    
    enrol = {}
    
    for stat in college_stats:
        to_parse = lxml.html.fromstring(stat)
        value = to_parse.xpath('//h2')
        label = to_parse.xpath('//h6')
        
        enrol[label] = value
    print "Enrolment stats:"
    print enrol
    
    scraperwiki.sqlite.save(unique_keys=['url'], 
                            data={
                                "name": college_name,
                                "url": college_url,
                                "address": college_address,
                                "city": college_city,
                                "postalcode": college_postalcode,
                                "nr_campus": college_nrcampuses,
                                "enrol_fulltime": enrol.get('Full-time', None),
                                "enrol_parttime": enrol.get('Part-time', None),
                                "enrol_international": enrol.get('International', None),
                                "enrol_apprentice": enrol.get('Apprentice', None),
                                "enrol_indigenous": enrol.get('Indigenous', None)
                                })

# # Read in a page
html = scraperwiki.scrape("http://www.collegesinstitutes.ca/our-members/member-directory/")
#
# # Find something on the page using css selectors
root = lxml.html.fromstring(html)
links = root.xpath('//ul[@class="facetwp-results"]/li/a/@href')

for link in links:
    print "Begin scraping page %s" % link
    parse_page(link)

#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
