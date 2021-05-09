<h2>SteamMarket bot with Telegram bot</h2>
This program requests data from Steam Market and calculates the average prices and quantities sold for given items for given dates.

<h3>What exactly does it do</h3>
data_gathering_for_custom_items.py first takes a game_id which the user wants to check the items for, then it sets cookies using STEAM_LOGIN_SECURE. This is a unique and private key, so the user has to provide their own key.
<br>Then it initiates it and takes a list of items which the user wants the data for. The list is prefilled with 25 items from CS:GO so that the user knows what format the names must be in and can test the app quickly, but those can be easily edited.
<br>After that item_prices() and item_quantity() functions are started, and they each send a request based on the game_id provided earlier. These functions use the SteamMarket library.
<br>All the prices are averaged and quantities summed for every unique day.
<br>Then some output is printed(average price today, percentage price change, etc.) and an fstring is returned(it's needed for the telegram_bot.py).
<br>The program repeats itself in the loop for as long as there are items in the list, then finishes.

<h3>Telegram bot</h3>
telegram_bot.py once again takes the items' names list, an api_key for the Telegram bot, and a chat_id for the chat which we want to send the data in.
<br>It then starts a loop, which takes the data from item_prices() and item_quantity() functions and transforms it into a url.
<br>The url gets sent in a request, and the loop continues. The user can freely change the sleep() function's argument however They want.

<h3>Purpose of this program</h3>
The purpose is to automate the process of checking the price and quantity data for items on the Steam Market.
<br>It's mainly useful to people who are interested in selling and/or buying items from the Steam Market.
