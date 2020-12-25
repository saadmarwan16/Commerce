<h1 align="center">Commerce</h1>

<br>

<h2 align="center">Overview</h2>

<p>Commerce is web application similar in spirit to eBay built with django. It is an e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”</p>

<h2 align="center">Features</h2>
 
 <p><b>Models:</b> The application has 5 models(tables): one for users, one for auction listings, one for bids, one for watchlist and one for comments made on auction listings.</p>
 
 <p><b>Login and Sign Up:</b> Users can register for a new account and also login into their account if they provide the right information.</p>
 
 <p><b>Create Listing:</b> Users can to visit a page to create a new listing. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users can also optionally be able to provide an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).</p>
 
 <p><b>Active Listings Page:</b> The default route of the web application lets users view all of the currently active auction listings. For each active listing, the page will display the title, description, current price, and photo (if one exists for the listing).</p>
 
 <p><b>Listing Page:</b> Clicking on a listing takes the users to a page specific to that listing. On that page: users can view all details about the listing, including the current price for the listing. If the user is signed in, the user can add the item to their “Watchlist.” If the item is already on the watchlist, the user can remove it.
If the user is signed in, the user can bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user will be presented with an error.
If the user is signed in and is the one who created the listing, the user have the ability to “close” the auction from the page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
If a user is signed in on a closed listing page, and the user has won that auction, the page will say so.
Users who are signed in can add comments to the listing page. The listing page also displays all comments that have been made on the listing.</p>
 
 <p><b>Watchlist:</b> Users who are signed in can visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.</p>
 
 <p><b>Categories:</b> Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.</p>
