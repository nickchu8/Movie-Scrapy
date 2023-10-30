# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/545611-everything-everywhere-all-at-once/']

    def parse(self, response):
        '''
        Start on a movie page, then navigate to the Full Cast & Crew page: which is just movie_url/cast.
        '''
        url = 'https://www.themoviedb.org/movie/545611-everything-everywhere-all-at-once/cast' #url for movie's cast page
        yield scrapy.Request(url, callback = self.parse_full_credits) #go to cast page

    def parse_full_credits(self, response):
        '''
        Start on full cast and crew page. yield scrapy.request for the page of each actor listed on the page, not including crew members.
        '''

        actors = response.css('ol.people.credits:not(.crew) a::attr(href)').getall() #list of actors using html tags and response
        for actor in actors: #iterate through list of actors and go to each actor's page
            yield response.follow(actor, callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        '''
        start on page of an actor. Yield a dictionary in the format of {"actor": actor_name, "movie_or_TV_name": movie_or_TV_name}
        Yield one such dictionary for each of the movies or TV shows on which that actor worked. 
        '''
        actor_name = response.css("h2 a::text").get() #get actor name by getting the a tags 
        print(actor_name)
        # iterate through all movies in actor's credit list and make a dictionary for each credit.
        for movie_or_TV_name in response.css("div.credits_list bdi::text").getall():
            yield {
                "actor": actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }