# FIND THE BEST FLIGHT (15%)
_You have been assigned to develop a system to help the end user to find the best flight to use when there is no direct flight available. The system will recommend the end user the best flight only based on route and political sentiment of the country. The best flight does not necessarily base on the shortest route but also considering the political situation each country the flight transited. Please note that there is no price of ticket involved in this recommendation system._ 

1.	Get and mark locations of 5- 10 major cities in the world (where you can easily gets their main English newspaper online) from Kuala Lumpur 
    1.	Guide 1: you can use Python Geocoding Toolbox
    Look up: https://pypi.python.org/pypi/geopy#downloads
    2.	Guide 2: you can use gmplot
        Lookup: https://github.com/vgm64/gmplot 
2.	Get the distances between these cities 
    1.	Guide 1: you can use Python Geocoding Toolbox
    2.	Suggestion 2: you should use Google Distance Matrix API
        1.	Login to the google developer’s website and follow through the examples. It is important that you know how to use the API key given to you within the code that you are going to use. Refer to this link: https://developers.google.com/maps/documentation/distance-matrix/start
3.	Using one of the algorithms for shortest path, get the minimum distance to travel to the destination from Kuala Lumpur by transiting 2-3 cities. 
4.	Plot line between the cities before and after the algorithm chosen.
    1.	Guide1:  you can use google.maps.Polyline. You can refer to this link:
https://www.sitepoint.com/create-a-polyline-using-the-geolocation-and-the-google-maps-api/
5.	Extract from the English newspaper of the cities of webpages text and count the number of words in the webpages.
    1.	Sometimes a webpage must be converted to the text version before it can be done
        1.	Guide 1: You may refer to this website to extract word from a website
https://www.textise.net/ 
        2.	Guide 2: You may refer to this website on how to count word frequency in a website
https://programminghistorian.org/lessons/counting-frequencies 
    2.	You can also filter stops words from the text you found
        1.	Guide 3: Stops words are such as conjunctions and prepositions. You may refer to this link: https://www.ranks.nl/stopwords 
        2.	Program using Rabin-karp algorithm to find and delete the stop words.
6.	Plot line/scatter/histogram graphs related to the word count using Plotly (Word count, stop words)
    1.	Guide 3: You may refer this link on how to install Plotly and how to use the API keys
 http://www.instructables.com/id/Plotly-with-Python/ 
https://plot.ly/python/getting-started/ 
7.	Compare words in the webpages with the positive, negative and neutral English words using a String Matching algorithm
    1.	Guide 4: Use the following word as positive and negative English words
http://positivewordsresearch.com/list-of-positive-words/
http://positivewordsresearch.com/list-of-negative-words/ 
    2.	Put these words in a text file for you to access them in your algorithm
    3.	Words that are not in the list can be considered as neutral
8.	Plot histogram graphs of positive and negative words found in the webpages.
    1.	Guide 5: Use Plotly
9.	Give an algorithmic conclusion regarding the sentiment of those articles
    1.	Guide 6: If there are more positive words, conclude that the article is giving positive sentiment, if there are more negative words, conclude that the article is giving negative sentiment.
        1.	You may try to conclude in different perspectives such as whether the list of positive and negative words above is accurate to be used in the context of the article you extracted the text.
        2.	Based on the conclusion, you may say the country has positive or negative political situation. 
10.	Lastly, calculate the total probability distribution of random routes taken for the end user to travel from Kuala Lumpur to other country.

## News Source
### London
1. London Marathon chiefs probe 'horrific' treatment of slowest runners called 'fat' and told to 'hurry up'
https://www.standard.co.uk/news/london/london-marathon-chiefs-probe-horrific-treatment-of-slowest-runners-a4132221.html
2. Richmond fire: 100 firefighters battle blaze at hotel and spa in south-west London
https://www.standard.co.uk/news/london/richmond-fire-100-firefighters-battle-blaze-at-hotel-spa-in-southwest-london-a4130816.html
3. Seagull that keeps landing on TfL traffic camera becomes internet hit
https://www.standard.co.uk/news/london/seagull-that-keeps-landing-on-tfl-traffic-camera-becomes-internet-hit-a4130416.html
4. West Drayton fire: Smoke visible for miles as huge blaze breaks out near Heathrow Airport
https://www.standard.co.uk/news/london/west-drayton-fire-smoke-visible-for-miles-as-huge-blaze-breaks-out-near-heathrow-airport-a4128526.html
5. Nail bomb haunts me 20 years on, says survivor of Brick Lane blast
https://www.standard.co.uk/news/london/nail-bomb-haunts-me-20-years-on-says-survivor-of-brick-lane-blast-a4127096.html
6. Man knifed in broad daylight attack next to Brunel University London campus in Uxbridge
https://www.standard.co.uk/news/crime/man-knifed-in-broad-daylight-attack-next-to-brunel-university-london-campus-in-uxbridge-a4128081.html

### Beijing
1. CFLD business expanding fast, signals confidence in domestic market
http://www.globaltimes.cn/content/1147419.shtml
2. Employees share their attitudes toward overtime working culture
http://www.globaltimes.cn/content/1147215.shtml
3. China to upskill workforce to expand employment
http://www.globaltimes.cn/content/1148172.shtml
4. African community in China
http://www.globaltimes.cn/content/1147096.shtml
5. ‘Death education’
http://www.globaltimes.cn/content/1144525.shtml

### Tokyo
1. Two teens arrested in Osaka for allegedly stretching rope across a road, injuring a motorcyclist
https://www.japantimes.co.jp/news/2019/05/02/national/two-teens-arrested-woman-injured-rope-across-road/#.XM0aaegzYgw
2. Nearly 80% in Japan support having women on throne and 82% feel affection for new emperor
https://www.japantimes.co.jp/news/2019/05/02/national/nearly-80-japan-support-women-throne-82-feel-affection-new-emperor-poll/#.XM0aXOgzYgw
3. North Korea fires several rounds of short-range 'projectiles' into Sea of Japan, South Korea says
https://www.japantimes.co.jp/news/2019/05/04/asia-pacific/north-korea-fires-several-rounds-short-range-missiles-sea-japan-south-korea-says/#.XM0aNOgzYgw
4. Woman has bag snatched after pulling ¥10 million from bank
https://www.tokyoreporter.com/japan/woman-has-bag-snatched-after-pulling-10-million-from-bank/
5. Trade ministry official arrested for attempting to smuggle stimulant
https://japantoday.com/category/crime/trade-ministry-official-arrested-for-attempting-to-smuggle-stimulant

### Los Angeles
1. Bomb threat cancels classes at South LA’s Locke High School; prom will go on
https://www.dailynews.com/2019/05/03/bomb-squad-searches-south-la-high-school-in-wake-of-threat/
2. In celebrations across LAUSD, San Fernando Valley high schools do #collegesigningday
https://www.dailynews.com/2019/05/03/in-celebrations-across-lausd-san-fernando-valley-high-schools-do-collegesigningday/
3. Homeless man arrested near Griffith Observatory in connection with Palmdale triple homicide
https://www.dailynews.com/2019/05/03/homeless-man-arrested-near-griffith-observatory-in-connection-with-palmdale-triple-homicide/
4. LA City Council approves reforms to city sexual harassment policies
https://www.dailynews.com/2019/05/03/la-city-council-approves-reforms-to-city-sexual-harassment-policies/
5. Religion events in the San Fernando Valley area, May 4-11
https://www.dailynews.com/2019/05/03/religion-events-in-the-san-fernando-valley-area-may-4-11/

### France
1. Clashes as May Day protesters march in cities across Europe
https://www.theguardian.com/world/2019/may/01/clashes-may-day-protesters-march-cities-across-europe-paris
2. Why delays and cancellations on France's rail network are the 'worst ever'
https://www.thelocal.fr/20190419/delays-and-cancellations-on-frances-rail-network-are-worst-ever
3. Climbers brought in to help protect Notre Dame from elements
https://www.theguardian.com/world/2019/apr/23/notre-dame-fire-climbers-brought-in-help-protect-elements-paris
4. Parisians and President Macron salute the city's firefighters
https://www.theguardian.com/world/2019/apr/18/parisians-and-president-macron-salute-the-citys-firefighters
5. Low-stakes European election in France – but not for Macron and Le Pen
https://www.france24.com/en/20190503-european-election-france-macron-le-pen-yellow-vests

### Germany
1. Germans take to streets in rent rise protests demanding more homes to become social housing
https://www.euronews.com/2019/04/06/germans-take-to-streets-in-rent-rise-protests-demanding-government-takeover-large-private
2. German police arrest ten suspects over alleged terrorist attack plot
https://www.euronews.com/2019/03/22/german-police-arrest-ten-suspects-over-alleged-terrorist-attack-plot
3. Why Frankfurt’s plan to build Europe’s biggest airport is making locals so angry
https://www.thelocal.de/20190503/why-frankfurts-plan-to-build-europes-biggest-airport-is-making-locals-so-angry
4. Germany's climate protesting youth take fight to RWE
https://www.thelocal.de/20190503/germanys-climate-protesting-youth-take-fight-to-rwe
5. German police shut down major 'darknet' illegal trading site
https://www.thelocal.de/20190503/german-police-shut-down-major-darknet-illegal-trading-site


### Hong Kong
1. The Umbrella Movement trial: Jailed for not apologising? Isn’t that a bit political?
https://www.hongkongfp.com/2019/05/03/hong-kongs-umbrella-movement-trio-appeals-conviction-sentence/
2. Hong Kong education chief says law for special needs students unnecessary despite lawmakers’ proposal
https://www.hongkongfp.com/2019/05/03/hong-kong-education-chief-says-law-special-needs-students-unnecessary-despite-lawmakers-proposal/
3. Hong Kong gov’t dental clinic loses personal information of nearly 400 patients
https://www.hongkongfp.com/2019/05/03/hong-kong-govt-dental-clinic-loses-personal-information-nearly-400-patients/
4. Hong Kong plastic surgeon whose patient died after Botox injections to face prosecution
https://www.scmp.com/news/hong-kong/law-and-crime/article/3008840/hong-kong-plastic-surgeon-whose-patient-died-after
5. Extradition bill sparks paralysing row in Hong Kong’s legislature
https://www.scmp.com/news/hong-kong/politics/article/3008333/extradition-bill-sparks-paralysing-row-hong-kongs

### Kuala Lumpur
1. 'Govt will reclaim land if it is owned by Johor Sultan'
https://www.nst.com.my/news/nation/2019/05/485437/govt-will-reclaim-land-if-it-owned-johor-sultan
2. KL, Canberra step up gender equality discussions
https://www.nst.com.my/news/nation/2019/05/485369/kl-canberra-step-gender-equality-discussions
3. Rally leaders speak up for Malay rulers, demand justice for deceased fireman Adib
https://www.thestar.com.my/news/nation/2019/05/04/rally-leaders-speak-up-for-malay-rulers/
4. Health Ministry launches new five year anti-smoking campaign
https://www.thestar.com.my/news/nation/2019/05/04/health-ministry-launches-new-five-year-anti-smoking-campaign/
5. DBKL to pay RM3 for every rat caught at Jinjang Utara market
https://www.thestar.com.my/metro/metro-news/2019/05/04/dbkl-to-pay-rm3-for-every-rat-caught-at-jinjang-utara-market/

### Atlanta, USA
1. SATURDAY’S WEATHER-TRAFFIC: Cloudy morning to build to potentially severe storms
https://www.ajc.com/weather/saturday-weather-traffic-cloudy-morning-build-potentially-severe-storms/qGCkhyzdTOh3cZG3iCBLUJ/
2. Atlanta —yet again —is named one of the worst places to commute by transit or car in recent ranking
https://www.ajc.com/news/world/atlanta-yet-again-named-one-the-worst-places-commute-transit-car-recent-ranking/Yfv86up06oBlC6y9YEpWKJ/
3. 82 arrested in multistate child exploitation sting
https://www.ajc.com/news/crime--law/breaking-arrested-multistate-child-exploitation-sting/yuwE4P0IVUFjkB7yzMpbsK/
4. Temp jobs play bigger role in Atlanta economy than rest of country
https://www.ajc.com/business/employment/temp-jobs-play-bigger-role-atlanta-economy-than-rest-country/m1FrNDAME9RET50bumeUMK/
5. These metro Atlanta companies are making big hires this May
https://www.ajc.com/business/employment/these-metro-atlanta-companies-are-making-big-hires-this-may/K6b9ixmPqj5y0QoZlgdhGP/


### Amsterdam, Netherlands
1. AMSTERDAM STUDENT CAMPUSES UNSAFE, STUDENT UNION SAYS
https://nltimes.nl/2019/05/03/amsterdam-student-campuses-unsafe-student-union-says
2. AMSTERDAM BILLBOARDS TO TURN INTO WAR MONUMENTS FOR REMEMBRANCE DAY
https://nltimes.nl/2019/05/03/amsterdam-billboards-turn-war-monuments-remembrance-day
3. AMSTERDAM TASK FORCE TO DEAL WITH EXPLOSIVES LEFT AT BUSINESSES
https://nltimes.nl/2019/04/29/amsterdam-task-force-deal-explosives-left-businesses
4. AMSTERDAM RANKED 4TH BEST TECH CITY IN THE WORLD
https://nltimes.nl/2019/02/06/amsterdam-ranked-4th-best-tech-city-world
5. SCOOTER BAN ON AMSTERDAM BIKE PATHS BEGINS MONDAY
https://nltimes.nl/2019/04/05/scooter-ban-amsterdam-bike-paths-begins-monday

