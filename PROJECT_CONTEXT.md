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







