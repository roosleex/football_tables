Use FastAPI for the backend
and vite react with typescript for the frontend for creating this appliction.

I want my new appliction get information for a user about main European football leagues standings

----------

I want this app to do api request every minute with standings data and on the main page to show date and time of last standings updation

----------

in the project root create sqlite db and every minute load there all standings
for user give away data from sqlite db

----------

Compute real form — fetch `GET /competitions/{code}/matches?status=FINISHED` (recent matchdays) in the refresher and derive each team's last‑5. This makes the column meaningful but adds a few more API calls per league (and some edge cases like postponed games).

----------

Add to the .env file setting MAX_REQUESTS_PER_MINUTE and set it to 10
and from now implement requests queue for all leagues. Update every league
considering  MAX_REQUESTS_PER_MINUTE setting and do requests every minute not greater than MAX_REQUESTS_PER_MINUTE. If app exceeded value of MAX_REQUESTS_PER_MINUTE then await for the next minute. When the next minute started then continue updating standings

----------

Add to the top of the app page the select for language changing
Add two languages for the app
English and Ukrainian
Also set teams names depends on current app language

----------

Add to the menu standings of all top European leagues, except second leagues, that available on football-data.org

----------

Using another API https://openfootapi.com/
add to the menu standings of Ukrainian league.
Add ukrainian language for Ukrainian league.

For https://openfootapi.com/ use settings from .env
FOOTAPI_MAX_REQUESTS_PER_MINUTE
OPENFOOT_API_KEY

----------

Add on the main page flexbox with items where every item contains every league top 3 team names and theirs points.
When I enter the main page I want see main menu with all leagues items on the left of the page with 25% of total width and flexbox with items on the right
of the page with 75% of total width. 
No table on the main page, only flexbox with items where every item contains every league top 3 team names and theirs points.
Then when I click on the menu item 75% right part will show me specified league full table. When I click on the top left brand section I will go to the main page

----------

Using https://openfootapi.com/ API
add to the menu standings of Belgium league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Turkey league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Greece league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Czech Republic league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Poland league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Norway league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Denmark league.
Add ukrainian language for newly added league.

----------







