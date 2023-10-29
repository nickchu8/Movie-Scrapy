# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/545611-everything-everywhere-all-at-once/']

    def parse(self, response):
        '''
        Start on a movie page, then navigae to the Full Cast & Crew page: which is just movie_url/cast.
        Once there, parse_full_credits() should be called, by specifying this method in the callback argument to a yielded scrapy.Request. Parse() does not return data
        No more than 5 lines of code
        '''
        
        yield scrapy.Request('https://www.themoviedb.org/movie/545611-everything-everywhere-all-at-once/cast', callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        '''
        Start on full cast and crew page. yield scrapy.request for the page of each actor listed on the page, not including crew members.
        yielded request specifies method parse_actor_page(self, response) should be called when actor's page is reached.
        parse_full_credits() does not return data, should be done in no more than 5 lines of code
        '''

        actors = response.css('ol.people.credits:not(.crew) a::attr(href)').getall()
        for actor in actors:
            yield response.follow(actor, callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        '''
        start on page of an actor. Yield a dictionary in the format of {"actor": actor_name, "movie_or_TV_name": movie_or_TV_name}
        Yield one such dictionary for each of the movies or TV shows on which that actor worked. 
        Note: need to determine both name of the actor and the name of the movie or show. no morethan 15 lines
        '''
        actor_name = response.css("h2 a::text").get() #get actor name by getting the a tags 
        # iterate through all movies in actor's credit list and make a dictionary for each credit.
        for movie_or_TV_name in response.css("div.credist_list bdi::text").getall():
            yield{
                "actor": actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }