import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sweetbook_project.settings')
from operator import itemgetter
import django
django.setup()
from sweetbook.models import User, Event, Recipe, SavedRecipe, Comment
import datetime
from django.utils import timezone


def add_event(name, date, description, place, postcode, url):
    e = Event.objects.get_or_create (name = name)[0] 
    e.date = date
    e.description = description
    e.place = place
    e.postcode = postcode
    e.url = url
    e.save()
    return e

def add_user(username,events, password, firstname, surname, email,picture = None):
    u = User.objects.get_or_create(username = username, password=password)[0]
    u.firstname = firstname
    u.surname = surname
    u.email = email
    u.picture = picture
    for event in events:
    	u.events.add(event)
    u.save()
    return u

def add_recipe(name,ingredients,description,rating,cooktime,difficulty,last_modified,user, picture = None):
    r = Recipe.objects.get_or_create(name=name, user=user)[0]
  
    r.ingredients = ingredients

    r.description = description
    r.rating = rating
    r.cooktime = cooktime
    r.difficulty = difficulty
    r.last_modified = last_modified
    r.picture = picture
    r.save()
    return r

def add_comment(user, recipe, date, description):
	c = Comment.objects.get_or_create(user=user, recipe = recipe, description = description)[0]
	c.date = date
	c.save()

def add_saved_recipe(user, recipe):
	s = SavedRecipe.objects.get_or_create(user=user, recipe=recipe)[0]
	s.save()
def populate():

	# dictionary of events

	events = {"Cookie sale for charity":{
						"date": timezone.now() + datetime.timedelta(days=30),
						"description": "Welcome for the annual baking sale in Glasgow for rasing funds and awareness of the less fortunate people around the world. everyone is welcomed!",
						"place" : "Glasgow George Square Market",
						"postcode" : "G2 1AL",
						"url": "https://maps.google.com/maps?q=G2%201AL&amp;t=&amp;z=16&amp;ie=UTF8&amp;iwloc=&amp;output=embed",
						},
			"Home Baking competition":{
						"date" : timezone.now() + datetime.timedelta(days=11),
						"description" : "Test your cookies recipes in the annual Home baking competition. All entrants welcome. The judging will begin at 5 pm. Viistors also welcomed!",
						"place": "Royal Concert Hall Glasgow",
						"postcode" : "G2 3NY",
						"url" : "https://maps.google.com/maps?q=G2%203NY&amp;t=&amp;z=16&amp;ie=UTF8&amp;iwloc=&amp;output=embed",
			}
	}

	for event, event_data in events.items():
		add_event(event, event_data["date"],event_data["description"], event_data["place"], event_data["postcode"], event_data["url"])

	# each user has a list of recipes that they added on the website

	elliot_recipes = [{"name": "Chocolate cake",
					"ingredients": "225g/8oz plain flour, 350g/12½oz caster sugar, 85g/3oz cocoa powder, 1 tsp baking powder, 1 tsp bicarbonate of soda, 2 free-range eggs,250ml/9fl oz milk, 125ml/4½fl oz vegetable oil, 2 tsp vanilla extract,250ml/9fl oz boiling water, 200g/7oz plain chocolate, 200ml/7fl oz double cream",
					"description":
									"""For the cake, place all of the cake ingredients, except the boiling water, into a large mixing bowl. Using a wooden spoon, or electric whisk, beat the mixture until smooth and well combined.

									Add the boiling water to the mixture, a little at a time, until smooth. (The cake mixture will now be very liquid.)

									Divide the cake batter between the sandwich tins and bake in the oven for 25–35 minutes, or until the top is firm to the touch and a skewer inserted into the centre of the cake comes out clean.

									Remove the cakes from the oven and allow to cool completely, still in their tins, before icing.

									For the chocolate icing, heat the chocolate and cream in a saucepan over a low heat until the chocolate melts. Remove the pan from the heat and whisk the mixture until smooth, glossy and thickened. Set aside to cool for 1–2 hours, or until thick enough to spread over the cake.

									To assemble the cake, run a round-bladed knife around the inside of the cake tins to loosen the cakes. Carefully remove the cakes from the tins.

									Spread a little chocolate icing over the top of one of the chocolate cakes, then carefully top with the other cake.

									Transfer the cake to a serving plate and ice the cake all over with the chocolate icing, using a palette knife.""",
					"rating": 8.90,
					"cooktime":90,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(minutes=180)},


					{"name": "Chocolate and orange scones",
					"ingredients": "700g self-raising flour, 150g butter, 150g caster sugar, 2 large oranges, finely grated zest of both and juice of one orange, 150g chocolate drops, 200ml whole milk",

					"description": 
									"""Preheat the oven to 210C/400F/Gas 6. Lightly butter two baking trays.

    								Sift the flour into a bowl. Rub in the butter using your hands until the mixture resembles fine breadcrumbs. Stir in the sugar, chocolate drops and orange zest.

    								In a measuring jug, mix the milk with the juice of one orange. Add to the flour mixture gradually until the dough just comes together. You may not need all the liquid. Be careful not to overwork the scone dough.

    								Roll out the dough to approximately 2cm/1in thickness and cut out scones using a 5-6cm/2-2½in cutter.

    								Transfer the scones to the buttered baking trays, brush the tops with milk and bake in the centre of the oven for 10-12 minutes, or until risen and golden-brown.

    								Remove from the oven and cool on wire rack. Serve with clotted cream and satsumas.""",
					"rating": 7.20,
					"cooktime":30,
					"difficulty":"medium",
					"last_modified": timezone.now() - datetime.timedelta(days=10)},
					]

	sofia_recipes = [{"name": "Orange butterfly cakes",
					"ingredients":"100g baking spread, 100g caster sugar, 2 large free-range eggs, 100g self-raising flour, 1 level tsp baking powder, 1 orange, grated zest only, 3 tbsp orange curd, 50g soft butter,100g sifted icing sugar",

					"description": 
									"""Preheat the oven to 180C/160C Fan/Gas 4.

    								Put all the cake ingredients into a large bowl and beat well for 2-3 minutes, or until the mixture is well-blended and smooth. Fill each paper case with about 35g of mixture.

    								Bake in the preheated oven for about 15-20 minutes, or until the cakes are well risen and golden-brown. Lift the paper cases out of the bun tin and cool the cakes on a wire rack.

    								When cool, cut a disc from the top of each cake leaving a little gap around the edge and cut this slice in half. Spoon half a teaspoonful of orange curd in each.

    								To make the icing, beat the butter and icing sugar together until well blended. Pipe or spoon a swirl of buttercream on top of the orange curd and place the half slices of cake on top to resemble butterfly wings. Dust the cakes with icing sugar to finish.""",
					"rating": 4.2,
					"cooktime":20,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(days=2)},

					{"name": "Mary’s Victoria sandwich with buttercream",
					"ingredients":"    4 large free-range eggs, 225g caster sugar, plus extra for sprinkling, 225g self-raising flour, 1 level tsp baking powder, 325g unsalted butter, 200g raspberries, 250g jam sugar, 200g icing sugar, 2 tbsp milk",

					"description":
								"""Break the eggs into a large mixing bowl, add the sugar, flour, baking powder and soft butter. Mix everything together until well combined. Be careful not to over-mix – as soon as everything is blended you should stop. The finished mixture should be of a soft ‘dropping’ consistency.

Divide the mixture evenly between the tins. Use a spatula to remove all of the mixture from the bowl and gently smooth the surface of the cakes.

Place the tins on the middle shelf of the oven and bake for 25 minutes. Don’t be tempted to open the door while they’re cooking, but after 20 minutes do look through the door to check them.

While the cakes are cooking, make the jam. Put the raspberries in a small deep-sided saucepan and crush them with a masher. Add the sugar and bring to the boil over a low heat until the sugar has melted. Increase the heat and boil for 4 minutes. Remove from the heat and carefully pour into a shallow container. Leave to cool and set.

The cakes are done when they’re golden-brown and coming away from the edge of the tins. Press them gently to check – they should be springy to the touch. Remove them from the oven and set aside to cool in the tins for 5 minutes. Then run a palette or rounded butter knife around the inside edge of the tin and carefully turn the cakes out onto a cooling rack.

To take your cakes out of the tins without leaving a wire rack mark on the top, put the clean tea towel over the tin, put your hand onto the tea towel and turn the tin upside-down. The cake should come out onto your hand and the tea towel – then you can turn it from your hand onto the wire rack. Set aside to cool completely.

For the buttercream, beat the butter in a large bowl until soft. Add half of the icing sugar and beat until smooth. Add the remaining icing sugar and one tablespoon of the milk and beat the mixture until creamy and smooth. Add the remaining tablespoon of milk if the buttercream is too thick. Spoon the buttercream into a piping bag fitted with a plain nozzle.

To assemble, choose the sponge with the best top, then put the other cake top-down on to a serving plate.""",
					"rating": 9.9,
					"cooktime":50,
					"difficulty":"difficult",
					"last_modified": timezone.now() - datetime.timedelta(days=1)},

					{"name": "Apple pie",
					"ingredients":"    255g plain flour, pinch of salt, 140g butter, 6 tsp cold water, 3 large Bramley cooking apples, chopped, stewed and cooledsugar, to taste",
					"description":
									"""Preheat the oven to 200C/400F/Gas 6. Sieve the flour and salt into a bowl.

    Rub in the margarine or butter until the mixture resembles fine breadcrumbs.

    Add the cold water to the flour mixture. Using a knife, mix the water into the flour, using your hand to firm up the mixture.

    Divide the pastry into two halves. Take one half and roll it out so that it is big enough to cover an 20cm/8in enamel or aluminium plate. Trim the edges with a knife using the edge of the plate as your guide.

    Cover the pastry with the stewed apples and sprinkle with sugar to taste.

    Roll out the other half of the pastry. Moisten the edge of the bottom layer of pastry and place the second piece on top.

    Press down on the pastry edges, making sure that they are properly sealed. Trim off any excess pastry with a knife in a downward motion, again using the plate as your guide.

    Flute the edges with a pinching action using your fingers and thumb.

    Prick the surface of the pastry lightly before placing the pie in the oven. Cook for 20-30 minutes.

    When the pie is cooked it should move slightly on the plate when gently shaken.

    Slide on to a serving plate, dust with caster sugar and serve.""",
					"rating": 8.60,
					"cooktime":40,
					"difficulty":"measy",
					"last_modified": timezone.now() - datetime.timedelta(hours=12)}]
	james_recipes = [{"name": "Steamed syrup sponge pudding",
					"ingredients":"    175g butter, softened, plus extra for greasing, 100g golden syrup, 125g golden caster sugar, 1 unwaxed lemon, zest only, 3 free-range eggs, lightly beaten, 175g self-raising flour, custard",

					"description": """
									Put the large pan on the hob and the steamer or egg box in the base. Cut 2 equal-size squares of foil and non-stick baking paper big enough to easily cover the top and rim of the basin. Lay the foil over the paper and fold a sharp pleat across the centre (to let the pudding expand as it cooks). Boil a full kettle.
Oil the pudding basin well, then pour in the syrup and agave nectar. Scatter over the breadcrumbs. In a large mixing bowl, whisk the eggs and sugar with an electric mixer for 4-5 minutes until light and moussey. Beat in the yogurt on a slower speed until just combined. Stir in the lemon zest, then sift in the flour and ginger. Fold in using a balloon whisk until smooth.
Working fairly quickly, gently transfer the mixture to the pudding basin so it rests on top of the syrup. Smooth the top, then place the baking paper/foil on top and secure with string – it should be as tight as you can get it. Snip off the foil and paper 2cm below the string. Make a handle with more string, then lower the pudding into the pan onto the steamer or egg box. Carefully pour just-boiled water into the pan to reach halfway up the sides of the basin. Put the lid on and steam over a medium heat for 1 hour 30-40 minutes, checking occasionally to make sure it isn’t boiling dry. Top up with boiling water as necessary.
The sponge is cooked when a skewer pushed through the foil into the middle of the sponge comes out clean.""",
					"rating": 5.70,
					"cooktime":20,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(days=4)}]

	# users list with the events they are participating in and the lists of recipes

	users = { "elliotmich": { "events":[Event.objects.get(name="Cookie sale for charity"),Event.objects.get(name="Home Baking competition")],
	                    	"password":"a",
	                    	"firstname":"Elliot",
	                    	"surname":"Michael",
	                    	"recipes": elliot_recipes,
	                    	"email" : "elliotmich@gmail.com"
							},
			"sofiabr98": { "events":[Event.objects.get(name="Home Baking competition")],
	                    	"password":"b",
	                    	"firstname":"Sofia",
	                    	"surname":"Brown",
	                    	"recipes": sofia_recipes,
	                    	"email" : "sofiabr98@gmail.com"
							},
			"jameswatt22": { "events":[Event.objects.get(name="Cookie sale for charity")],
	                    	"password":"c",
	                    	"firstname":"James",
	                    	"surname":"Watt",
	                    	"recipes": james_recipes,
	                    	"email": "jameswatt22@yahoo.com"
							},
			"mariaj": { "events":[Event.objects.get(name="Cookie sale for charity")],
	                    	"password":"d",
	                    	"firstname":"Maria",
	                    	"surname":"Jones",
	                    	"recipes": [],
	                    	"email": "mariajones@yahoo.com"
							}


	}

	
	# add users and the recipes they created
	for user, user_data in users.items():
		u = add_user(user,users[user]["events"], users[user]["password"], users[user]["firstname"], users[user]["surname"],users[user]["email"])
		for recipe in user_data["recipes"]:
			r = add_recipe(recipe["name"], recipe["ingredients"],recipe["description"],recipe["rating"],recipe["cooktime"],recipe["difficulty"], recipe["last_modified"],u)


	# add some comments 
	elliot = User.objects.get(username="elliotmich")
	sofia = User.objects.get(username="sofiabr98")
	maria = User.objects.get(username="mariaj")

	add_comment(elliot, Recipe.objects.get(name="Orange butterfly cakes", user=sofia), timezone.now() - datetime.timedelta(days=4),
		"Made it today! Very easy to prepare and tastes amazing!!!")
	add_comment(maria, Recipe.objects.get(name="Orange butterfly cakes"), timezone.now() - datetime.timedelta(hours=2),
		"Hi! I am a student and I tried this recipe with my flatmates a week ago! Delicious, everyone loved it!")
	add_comment(maria, Recipe.objects.get(name="Chocolate cake"), timezone.now() - datetime.timedelta(minutes=20),
		"Pretty plain, but 	very easy to make.I don t think will do it again")
	add_comment(elliot, Recipe.objects.get(name="Steamed syrup sponge pudding"), timezone.now() - datetime.timedelta(days=2),
		"It s supposed to be easy but I managed to screw it up lol")

	# make some users save some recipes

	add_saved_recipe(elliot,Recipe.objects.get(name="Steamed syrup sponge pudding"))
	add_saved_recipe(elliot,Recipe.objects.get(name="Apple pie"))
	add_saved_recipe(elliot,Recipe.objects.get(name="Mary’s Victoria sandwich with buttercream"))
	add_saved_recipe(sofia, Recipe.objects.get(name="Chocolate cake"))
	add_saved_recipe(maria,Recipe.objects.get(name="Apple pie"))
	add_saved_recipe(maria,Recipe.objects.get(name="Chocolate cake"))




if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()

