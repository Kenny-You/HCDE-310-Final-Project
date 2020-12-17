from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json
import logging
import random

app = Flask(__name__)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('index.html') 

@app.route("/start")
def emotion_handler():
    app.logger.info("In DrinkTypeHandler")
    return render_template('AlcoholType.html')
        
@app.route("/alctype")
def alc_type_handler():
    drink_type = request.args.get('alctype')
    app.logger.info(drink_type)
    if 'non-alcoholic' in drink_type:
        result = cocktail(param = {'a' : 'Non_Alcoholic'})
        drink_name = result['strDrink']
        drink_img = result['strDrinkThumb']
        drink_id = result['idDrink']
        return render_template('NonAlcCocktailResults.html', page_title = "Suggested Non-Alcoholic Cocktail", drink_name = drink_name, drink_img = drink_img, drink_id = drink_id)
    else:
        return render_template('EmotionSelection.html')

@app.route("/emotionresponse")
def drink_type_handler():
    emotion_type = request.args.get('emotion_type')
    app.logger.info(emotion_type)
    if 'happy' in emotion_type:
        result = cocktail(i = 'Tequila')
    elif 'sad' in emotion_type:
        result = cocktail(i = 'Gin')
    elif 'angry' in emotion_type:
        result = cocktail(i = 'Vodka')
    else:
        result = cocktail(i = 'Rum')
    drink_name = result['strDrink']
    drink_img = result['strDrinkThumb']
    drink_id = result['idDrink']
    return render_template('AlcCocktailResults.html', page_title = "List of Cocktails based on current emotion: %s"%emotion_type[0], drink_name = drink_name, drink_img = drink_img, drink_id = drink_id)

@app.route("/cocktaildetails")
def drink_detail_handler():
    drink_id = request.args.get('details')
    app.logger.info(drink_id)
    details = cocktaildetails(i = drink_id) #Dictionary of cocktail information
    drink_name = details['strDrink']
    drink_id = details['idDrink']
    drink_img = details['strDrinkThumb']
    drink_instructions = details['strInstructions']
    ingredients = []
    proportions = []
    for key, value in details.items():
        if 'Ingredient' in key and value != None:
            ingredients.append(value)
        if 'Measure' in key and value != None:
            proportions.append(value)

    return render_template('CocktailDetails.html', ingredients = ingredients, proportions = proportions, drink_name = drink_name, drink_img = drink_img, drink_instructions = drink_instructions)

def cocktail(baseurl = "https://www.thecocktaildb.com/api/json/v1/1/filter.php", a = '', i = '', api_key = '1', format = 'json', param = {}):
    param['i'] = i
    param['api_key'] = api_key
    param['format'] = format
    url = baseurl + "?" + urllib.parse.urlencode(param)
    c = urllib.request.urlopen(url)
    readc = c.read()
    cdata = json.loads(readc)
    drinks = []
    for data in cdata['drinks']:
        drinks.append(data)
    random_drink = random.choice(drinks)
    return random_drink

def cocktaildetails(baseurl = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php", a = '', i = '', api_key = '1', format = 'json', param = {}):
    param['i'] = i
    param['api_key'] = api_key
    param['format'] = format
    url = baseurl + "?" + urllib.parse.urlencode(param)
    c = urllib.request.urlopen(url)
    readc = c.read()
    cdata = json.loads(readc)
    drinks = []
    for data in cdata['drinks']:
        drinks.append(data)
    return cdata['drinks'][0]

if __name__ == "__main__":
    # Used when running locally only. 
	# When deploying to Google AppEngine, a webserver process will
	# serve your app. 
    app.run(host="localhost", port=8080, debug=True)