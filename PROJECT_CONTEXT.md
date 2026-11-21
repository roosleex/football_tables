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

Output leagues in menu in order according to the current UEFA rankings country coefficients. The same order apply also to the flexbox with items where every item contains every league top 3 team names and theirs points.

----------

When a user click on a flexbox item go to the related league standings table

----------

Add to the app cookies for saving user state.
Add to every flexbox item on the top right corner of an item cross sign for closing item. So user can close unnecessary flexbox items (boring leagues)
and next time when he open the site he will see only his remained items.
Use cookies to save such user state.
Also add to the left of the button "Languages" new button called "Reset settings" when a user wants to turn back all leagues

----------

Also remember in cookies last active language

----------

Add Ukrainian language for Portugal teams names

----------

Using https://openfootapi.com/ API
add to the menu standings of Cyprus league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Switzerland league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Austria league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Hungary league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Croatia league.
Add ukrainian language for newly added league.

----------

Text of span with css classes source-badge source-live set always to LIVE. Do not translate text of that span

----------

Set name of PPL (portugal league ) properly. Now it is called PPL and I do not understand what is PPL mean 

----------

Add horizontal scroll bar to the standings table when a user screen is narrow to be available
to scroll table horizontally on small screens

----------

Using https://openfootapi.com/ API
add to the menu standings of Sweden league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Scotland league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Romania league.
Add ukrainian language for newly added league.

----------

Using thesportsdb.com API
add to the menu standings of Czech Republic league.
Add ukrainian language for newly added league.
Use setting from .env THESPORTSDB_MAX_REQUESTS_PER_MINUTE
and do requests every minute not greater than THESPORTSDB_MAX_REQUESTS_PER_MINUTE

----------

Using https://openfootapi.com/ API
add to the menu standings of Azerbaijan league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Israel league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Slovenia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Slovakia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Bulgaria league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Serbia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Iceland league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Ireland league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Armenia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Latvia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Bosnia and Herzegovina league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Kosovo league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Finland league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Kazakhstan league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Liechtenstein league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Moldova league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Faroe Islands league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Albania league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of North Macedonia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Lithuania league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Gibraltar league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Andorra league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Malta league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Estonia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Georgia league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Northern Ireland league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Luxembourg league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Montenegro league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of Wales league.
Add ukrainian language for newly added league.

----------

Using https://openfootapi.com/ API
add to the menu standings of San Marino league.
Add ukrainian language for newly added league.

----------

Why in menu some countries have DEU or ENG
<span class="league-country">DEU</span> or 
<span class="league-country">ENG</span>
instead of full country name like 
<span class="league-country">Бельгія</span>
Fix it

----------

Why in mobile browser I see flags pictures but on my laptop browser I see some two characters like GB for Premier League or FR for Ligue 1 instead of flag pictures?
I want to see country flags both on mobile devices and laptops
Fix it 

----------

Rearrange main menu which is in the left side of the app.
I want current items to add to one big item called Europe. When a user clicks on Europe main menu item then subitems will open with all current items of european leagues. Also when a user clicks on Europe main menu item in the right part of app will show the flexbox with items where every item contains every league top 3 team names and theirs points of european leagues like it is viewed now.

----------

Now add to the main menu item called Asia.
Using https://openfootapi.com/ API
add to the main menu item called Asia standings of all asian leagues.
Add ukrainian language for newly added asian leagues.

----------

Check the app football_tables on security issues and vulnerabilities.
If you will find any fix them. 

----------

Check backend if all neccessary tests are existed.
Missed tests add to the /tests folder

----------

Now add to the main menu item called North America.
Using https://openfootapi.com/ API
add to the main menu item called North America standings of North America  leagues.
Add ukrainian language for newly added North America leagues.

----------

Now add to the main menu item called South America.
Using https://openfootapi.com/ API
add to the main menu item called South America standings of South America  leagues.
Add ukrainian language for newly added South America leagues.

----------







