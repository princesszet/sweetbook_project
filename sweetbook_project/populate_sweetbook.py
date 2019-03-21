import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sweetbook_project.settings')
from operator import itemgetter
import django
django.setup()
from sweetbook.models import UserProfile, Event, Recipe, SavedRecipe, Comment
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404

def add_event(name, date, description, place, postcode, url):
    e = Event.objects.get_or_create (name = name)[0] 
    e.date = date
    e.description = description
    e.place = place
    e.postcode = postcode
    e.url = url
    e.save()
    return e

def add_user(username, password, email):
    u = User.objects.get_or_create(username = username, password=password)[0]
    u.email = email
    return u

def add_userprofile(user,events, firstname, surname,picture = None ):
    u = UserProfile.objects.get_or_create(user = user)[0]
    u.firstname = firstname
    u.surname = surname
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
						"url": "https://osmaps.ordnancesurvey.co.uk/55.86039,-4.24987,15/pin",
						},
			"Home Baking competition":{
						"date" : timezone.now() + datetime.timedelta(days=11),
						"description" : "Test your cookies recipes in the annual Home baking competition. All entrants welcome. The judging will begin at 5 pm. Viistors also welcomed!",
						"place": "Royal Concert Hall Glasgow",
						"postcode" : "G2 3NY",
						"url" : "https://osmaps.ordnancesurvey.co.uk/55.86462,-4.25299,15/pin"
			},
			"Live cooking demonstrations":{
						"date" : timezone.now() + datetime.timedelta(days=2),
						"description" : "Don't miss the chance to watch the great Gordon Ramsay in a live cooking demonstration, along with other famous chefs guests. The theme for the cooking will be chesecake. Please purcase a ticket before!",
						"place": "Royal Concert Hall Glasgow",
						"postcode" : "G2 3NY",
						"url" : "https://osmaps.ordnancesurvey.co.uk/55.86462,-4.25299,15/pin"
			},
			"Baking classes":{
						"date" : timezone.now() + datetime.timedelta(days=6),
						"description" : "5-week baking course which involves a 3 hour weekly course for both beginners or advanced cooks who would like to learn more about the mix of favlours which make the perfect deserts.",
						"place": "Royal Concert Hall Glasgow",
						"postcode" : "G2 3NY",
						"url" : "https://osmaps.ordnancesurvey.co.uk/55.86462,-4.25299,15/pin"
			},
			"Cookie Fayre":{
						"date" : timezone.now() + datetime.timedelta(days = 30),
						"description" : "Come to the annual Cookies Fayre if you want to have an exotic taste of the worldwide famous bakery or even if you just want to try out the traditional grandmoms' chocolate cookies. Entrance is free, not the cookies though!",
						"place": "Glasgow University Main Gate",
						"postcode" : "G12 8QQ",
						"url": "https://osmaps.ordnancesurvey.co.uk/55.87175,-4.28836,15/pinch"
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
					"rating": 5,
					"cooktime":90,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(minutes=180),
					"picture":"recipes_images/chocolate-cake.jpg"},


					{"name": "Chocolate and orange scones",
					"ingredients": "700g self-raising flour, 150g butter, 150g caster sugar, 2 large oranges, finely grated zest of both and juice of one orange, 150g chocolate drops, 200ml whole milk",

					"description": 
									"""Preheat the oven to 210C/400F/Gas 6. Lightly butter two baking trays.

    								Sift the flour into a bowl. Rub in the butter using your hands until the mixture resembles fine breadcrumbs. Stir in the sugar, chocolate drops and orange zest.

    								In a measuring jug, mix the milk with the juice of one orange. Add to the flour mixture gradually until the dough just comes together. You may not need all the liquid. Be careful not to overwork the scone dough.

    								Roll out the dough to approximately 2cm/1in thickness and cut out scones using a 5-6cm/2-2½in cutter.

    								Transfer the scones to the buttered baking trays, brush the tops with milk and bake in the centre of the oven for 10-12 minutes, or until risen and golden-brown.

    								Remove from the oven and cool on wire rack. Serve with clotted cream and satsumas.""",
					"rating": 3.20,
					"cooktime":30,
					"difficulty":"medium",
					"last_modified": timezone.now() - datetime.timedelta(days=10),
					"picture":"recipes_images/chocolate-and-orange-scones.jpg"},


					{"name": "Cherry pie",
					"ingredients": "    150g good-quality black cherry jam, 100ml water, 1 tbsp ground arrowroot, mixed to a paste with 2 tbsp water, 750g fresh red cherries, 250g plain flour, 175g fridge-cold unsalted butter, 1 tbsp caster sugar, plus 2 tsp for topping, 1 large free-range egg, beaten, 1 tbsp cold water",
					"description":
									"""For the pie filling, heat the cherry jam and water in a pan over a low heat, stirring continuously, until the jam has melted and is starting to bubble.

Add the arrowroot mixture and stir to combine. Continue to simmer the mixture until the sauce is very thick and smooth.

Add the cherries and stir carefully to coat them in the hot jam mixture. Transfer the filling mixture to a 1 litre pint pie dish (they should reach just above the rim of the dish). Set aside to cool.

For the pastry, pulse the flour, butter and sugar together in a food processor until the mixture resembles fine breadcrumbs.

Mix together the beaten egg and water. Set aside one tablespoon of this mixture to use as a glaze. With the motor still running, gradually add the remaining egg and water mixture to the bowl of the food processor a little at a time, until the mixture comes together as a dough.

Roll out the pastry onto a lightly floured work surface until it is 7cm larger in diameter than the pie dish. Cut two or three long strips from the edges of the pastry (2.5cm/1in wide).

Brush the rim of the pie dish with a little of the reserved beaten egg. Lay the strips of pastry onto the rim of the pie dish, overlapping the strips slightly at the joins. (This will make a thicker edge for crimping.) Brush the pastry rim with more of the beaten egg.

Gently lift the rolled pastry, using the rolling pin, and place on top of the cherry filling. Press the pastry down at the edges to seal the layers of pastry together. Trim off any excess pastry, then crimp the edges with your fingertips.

Transfer the pie dish to a baking tray and chill in the fridge for 30 minutes. """,
					"rating": 4.2,
					"cooktime":90,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(minutes=180),
					"picture":"recipes_images/cherry-pie.jpg"},


					{"name": "Double chocolate cherry brownies",
					"ingredients": "350g dark chocolate , 250g unsalted butter, 3 large free-range eggs, 250g dark soft brown sugar, 110g plain flour, 1 tsp baking powder, 150g fresh cherries, 150g white chocolate, 1-2 tbsp cocoa powder",
					"description":
									""" Preheat the oven to 170C/150C Fan/Gas 3. Grease a 30x23cm/12x9in baking tin with butter then line the base and sides with baking paper.

    Heat the plain chocolate and butter in a saucepan over a low heat until just melted and well combined, stirring occasionally. Remove from the heat and set aside to cool slightly (at least 5 minutes).

    Meanwhile, whisk the eggs with the sugar in a large bowl until thick, pale and creamy.

    Whisk the cooled chocolate mixture into the egg mixture, then gently fold in the flour, baking powder and half the cherries until just combined.

    Spoon the brownie mixture into the prepared tin, then scatter over the white chocolate and the remaining cherries.

    Bake the brownies in the oven for 25-30 minutes, or until the surface is cracked and a skewer inserted into the centre of the brownies comes out with just a little mixture sticking to it. Remove from the oven and set aside to cool completely in the tin, on a wire rack.

    To serve, dust the brownies with cocoa powder, then cut into squares and remove from the tin. """,
					"rating": 2.9,
					"cooktime":90,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(days = 1),
					"picture":"recipes_images/double-chocolate-cherry-brownies.jpg"},
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
					"last_modified": timezone.now() - datetime.timedelta(days=2),
					"picture":"recipes_images/orange-butterfly-cakes.jpg"},

					{"name": "Mary’s Victoria sandwich with buttercream",
					"ingredients":"4 large free-range eggs, 225g caster sugar, plus extra for sprinkling, 225g self-raising flour, 1 level tsp baking powder, 325g unsalted butter, 200g raspberries, 250g jam sugar, 200g icing sugar, 2 tbsp milk",

					"description":
								"""Break the eggs into a large mixing bowl, add the sugar, flour, baking powder and soft butter. Mix everything together until well combined. Be careful not to over-mix – as soon as everything is blended you should stop. The finished mixture should be of a soft ‘dropping’ consistency.

Divide the mixture evenly between the tins. Use a spatula to remove all of the mixture from the bowl and gently smooth the surface of the cakes.

Place the tins on the middle shelf of the oven and bake for 25 minutes. Don’t be tempted to open the door while they’re cooking, but after 20 minutes do look through the door to check them.

While the cakes are cooking, make the jam. Put the raspberries in a small deep-sided saucepan and crush them with a masher. Add the sugar and bring to the boil over a low heat until the sugar has melted. Increase the heat and boil for 4 minutes. Remove from the heat and carefully pour into a shallow container. Leave to cool and set.

The cakes are done when they’re golden-brown and coming away from the edge of the tins. Press them gently to check – they should be springy to the touch. Remove them from the oven and set aside to cool in the tins for 5 minutes. Then run a palette or rounded butter knife around the inside edge of the tin and carefully turn the cakes out onto a cooling rack.

To take your cakes out of the tins without leaving a wire rack mark on the top, put the clean tea towel over the tin, put your hand onto the tea towel and turn the tin upside-down. The cake should come out onto your hand and the tea towel – then you can turn it from your hand onto the wire rack. Set aside to cool completely.

For the buttercream, beat the butter in a large bowl until soft. Add half of the icing sugar and beat until smooth. Add the remaining icing sugar and one tablespoon of the milk and beat the mixture until creamy and smooth. Add the remaining tablespoon of milk if the buttercream is too thick. Spoon the buttercream into a piping bag fitted with a plain nozzle.

To assemble, choose the sponge with the best top, then put the other cake top-down on to a serving plate.""",
					"rating": 4.9,
					"cooktime":50,
					"difficulty":"difficult",
					"last_modified": timezone.now() - datetime.timedelta(days=1),
					"picture":"recipes_images/marys-victoria-sandwich-with-buttercream.jpg"},

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
					"rating": 2.60,
					"cooktime":40,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(hours=12),
					"picture":"recipes_images/apple-pie.jpg"},

					{"name": "Salted chocolate cake",
					"ingredients": "    375g self-raising flour, 50g cocoa powder, 325g caster sugar, 4 free-range eggs, 375ml oz full-fat milk, 250g unsalted butter, 200g dark chocolate, 2 tsp vanilla extract, 250g soured cream, 400g milk chocolate,, 2 tsp black or regular sea salt flakes",
					"description":
									"""Place the flour, cocoa, sugar, eggs, milk, butter, melted dark chocolate and vanilla in a large bowl and whisk until smooth.

Evenly divide the mixture between the tins and bake for 35–40 minutes, or until cooked through and a skewer inserted into the middle of each cake comes out clean. Leave to cool slightly in the tins before turning out onto wire racks to cool completely.

Place the soured cream and melted milk chocolate in a large bowl. Stir to combine and refrigerate for 10 minutes, or until the ganache is a firm, spreadable consistency.

Place one of the cakes on a cake stand or plate and trim the top so it is flat. Spread the top of the cake with half of the ganache. Top with the remaining cake and cover the top of that cake with the rest of the ganache. Sprinkle the salt over the top of the cake.""",
					"rating": 4.90,
					"cooktime":120,
					"difficulty":"hard",
					"last_modified": timezone.now() - datetime.timedelta(days = 4),
					"picture":"recipes_images/salted-chocolate-cake.jpg"},

					{"name": "Mini apple and almond cakes",
					"ingredients": "75g butter, 100g self-raising flour, 100g caster sugar, 1 free-range egg, beaten, 1/2 tsp almond extract60g Bramley apples,15g flaked almonds, crème fraîche",
					"description":
									""" Preheat the oven to 180C/160C Fan/Gas 4.

    Grease the inside of the cooking rings with a little butter and dust with flour. Arrange the cooking rings on a baking sheet lined with baking paper.

    Pour the melted butter into a large bowl. Add the sugar, flour, egg and almond extract and mix together until combined.

    Spoon a little of the mixture into the base of each ring, arrange some of the apple slices over the batter and spoon the remaining cake mixture on top, levelling with the back of a teaspoon.

    Scatter each cake with flaked almonds. Bake for 25–30 minutes, or until well risen and golden-brown.

    Set aside to cool for about 10 minutes before removing the rings. Serve warm with a dollop of crème fraîche.""",
					"rating": 4,
					"cooktime":20,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(days = 1),
					"picture":"recipes_images/mini-apple-and-almond-cakes.jpg"},]
					


	james_recipes = [{"name": "Steamed syrup sponge pudding",
					"ingredients":"    175g butter, softened, plus extra for greasing, 100g golden syrup, 125g golden caster sugar, 1 unwaxed lemon, zest only, 3 free-range eggs, lightly beaten, 175g self-raising flour, custard",

					"description": """
									Put the large pan on the hob and the steamer or egg box in the base. Cut 2 equal-size squares of foil and non-stick baking paper big enough to easily cover the top and rim of the basin. Lay the foil over the paper and fold a sharp pleat across the centre (to let the pudding expand as it cooks). Boil a full kettle.
Oil the pudding basin well, then pour in the syrup and agave nectar. Scatter over the breadcrumbs. In a large mixing bowl, whisk the eggs and sugar with an electric mixer for 4-5 minutes until light and moussey. Beat in the yogurt on a slower speed until just combined. Stir in the lemon zest, then sift in the flour and ginger. Fold in using a balloon whisk until smooth.
Working fairly quickly, gently transfer the mixture to the pudding basin so it rests on top of the syrup. Smooth the top, then place the baking paper/foil on top and secure with string – it should be as tight as you can get it. Snip off the foil and paper 2cm below the string. Make a handle with more string, then lower the pudding into the pan onto the steamer or egg box. Carefully pour just-boiled water into the pan to reach halfway up the sides of the basin. Put the lid on and steam over a medium heat for 1 hour 30-40 minutes, checking occasionally to make sure it isn’t boiling dry. Top up with boiling water as necessary.
The sponge is cooked when a skewer pushed through the foil into the middle of the sponge comes out clean.""",
					"rating": 2.70,
					"cooktime":20,
					"difficulty":"medium",
					"last_modified": timezone.now() - datetime.timedelta(hours = 1),
					"picture":"recipes_images/steamed-syrup-sponge-pudding.jpg"},

					{"name": "Lemon and almond cake",
					"ingredients": "200g butter, 200g golden caster sugar, 3 large free-range eggs, 50g plain flour or white spelt flour, 125g ground almonds, 2 lemons, 1 lemon, juice only, 5-6 tbsp icing sugar",
					"description":
									"""In a mixing bowl cream together the butter and sugar until light and fluffy using an electric hand whisk or wooden spoon. Slowly beat in the eggs, one at a time. When the eggs are fully incorporated, fold in the flour, then the almonds and lemon zest.

Scrape the mixture into the tin and tap the sides to release any air bubbles. Bake for 35-40 minutes, or until the sponge is lightly golden-brown, coming away from the sides of the tin and a skewer inserted into the middle of the cake comes out clean.

While the cake is still hot and still in the tin, stab it with a chopstick or some such weapon all over the cake, making 15 or so holes. Drizzle the lemon juice into the holes and all over the cake then leave in the tin to cool.

When you're ready to serve the cake, make the icing. To make the icing, mix the lemon juice, a little at a time, into the icing sugar to make a smooth paste. Remove the cake from the tin and smooth the icing on the top, then serve.""",
					"rating": 3.8,
					"cooktime":30,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(hours = 2),
					"picture":"recipes_images/lemon-and-almond-cake.jpg"},

					{"name": "Carrot cake loaf",
					"ingredients": "140ml vegetable oil, 2 free-range eggs, 200g brown sugar, 300g grated carrot, 100g raisins, 75g pecans, 180g self-raising flour, 1 pinch salt, 1/2 tsp bicarbonate of soda, 1 tsp ground cinnamon, 1/2 tsp freshly grated nutmeg, 1/2 tsp mixed spice, 200g full-fat cream cheese, 50g butter, 50g icing sugar, 1 orange, zest only",
					"description":
									"""For the carrot cake, beat the eggs in a large bowl, then add the oil, brown sugar, grated carrot, raisins and chopped nuts.

Sift in the remaining cake ingredients and mix using a wooden or large metal spoon until well combined.

Pour the mixture into the prepared loaf tin, smooth the surface and bake for 1 hour 15 minutes, or until a skewer inserted into the middle comes out clean.

Remove from the oven and allow the cake to cool in the tin for about 5 minutes before removing. Cool completely on a wire rack before serving.

For the icing, beat the cream cheese and butter together in a bowl until well combined. Add the vanilla extract, icing sugar and orange zest and mix until the icing is smooth and thick. Using a palette knife, spread the icing evenly over the cooled cake, dipping the knife into a bowl of hot water if the icing is hard to spread out. Cut into slices to serve.""",
					"rating": 1.90,
					"cooktime":20,
					"difficulty":"easy",
					"last_modified": timezone.now() - datetime.timedelta(minutes=180),
					"picture":"recipes_images/carrot-cake-loaf.jpg"},]

	maria_recipes = [{"name": "Chocolate flapjacks",
					"ingredients": "200g unsalted butter, 300g golden syrup, 450g jumbo rolled porridge oats, pinch of plain flour, pinch salt, 200g dried apricots, 100g plain chocolate, broken into pieces",
					"description":
									"""Preheat the oven to 180C/160C Fan/Gas 4. Grease a 20cm/8in square cake tin with butter, then line the base and sides with baking parchment.

    Slowly bring the butter and syrup to the boil in a saucepan, stirring. Remove from the heat and stir in the oats and salt, then the dried apricots, until well combined.

    Scrape the mixture into the prepared tin, then press it into an even layer using the back of a wooden spoon. Bake for 45-50 minutes, or until golden-brown. Set aside to cool slightly in the tin, then run a round-bladed knife around the inside edges of the tin and cut the flapjack into squares. Set them aside to cool completely in the tin.

    Meanwhile, suspend a heatproof glass bowl over a saucepan of gently simmering water, making sure that the base of the bowl does not touch the water. Add the chocolate and stir until melted.

    Turn the cooled flapjacks out onto a wire rack and drizzle them with the melted chocolate. Set aside for a further 25-30 minutes, or until the chocolate has set.""",
					"rating": 5,
					"cooktime":120,
					"difficulty":"medium",
					"last_modified": timezone.now() - datetime.timedelta(days = 1),
					"picture":"recipes_images/chocolate-flapjacks.jpg"},
					]

	# users list with the events they are participating in and the lists of recipes

	users = { "elliotmich": { "events":[Event.objects.get(name="Cookie sale for charity"),Event.objects.get(name="Home Baking competition"),
	Event.objects.get(name="Live cooking demonstrations"),Event.objects.get(name="Baking classes")],
	                    	"password":"a",
	                    	"firstname":"Elliot",
	                    	"surname":"Michael",
	                    	"recipes": elliot_recipes,
	                    	"email" : "elliotmich@gmail.com"
							},
			"sofiabr98": { "events":[Event.objects.get(name="Home Baking competition"),Event.objects.get(name="Live cooking demonstrations"),
			Event.objects.get(name="Cookie Fayre")],
	                    	"password":"b",
	                    	"firstname":"Sofia",
	                    	"surname":"Brown",
	                    	"recipes": sofia_recipes,
	                    	"email" : "sofiabr98@gmail.com"
							},
			"jameswatt22": { "events":[Event.objects.get(name="Cookie sale for charity"),Event.objects.get(name="Baking classes"),
			Event.objects.get(name="Cookie Fayre")],
	                    	"password":"c",
	                    	"firstname":"James",
	                    	"surname":"Watt",
	                    	"recipes": james_recipes,
	                    	"email": "jameswatt22@yahoo.com"
							},
			"mariaj": { "events":[Event.objects.get(name="Baking classes"),Event.objects.get(name="Live cooking demonstrations"),
			Event.objects.get(name="Cookie Fayre")],
	                    	"password":"d",
	                    	"firstname":"Maria",
	                    	"surname":"Jones",
	                    	"recipes": maria_recipes,
	                    	"email": "mariajones@yahoo.com"
							},
			"martingreg": { "events":[Event.objects.get(name="Baking classes"),Event.objects.get(name="Cookie sale for charity"),
			Event.objects.get(name="Cookie Fayre")],
	                    	"password":"e",
	                    	"firstname":"Martin",
	                    	"surname":"Gregor",
	                    	"recipes": [],
	                    	"email": "martingreg@yahoo.com"
							}


	}

	
	# add users and the recipes they created
	for user, user_data in users.items():
		u = add_user(user, users[user]["password"], users[user]["email"])
		up = add_userprofile(u,users[user]["events"],users[user]["firstname"], users[user]["surname"])
		for recipe in user_data["recipes"]:
			r = add_recipe(recipe["name"], recipe["ingredients"],recipe["description"],recipe["rating"],recipe["cooktime"],recipe["difficulty"], recipe["last_modified"],u,recipe["picture"])


	# add some comments 
	elliot = User.objects.get(username="elliotmich")
	sofia = User.objects.get(username="sofiabr98")
	maria = User.objects.get(username="mariaj")
	james = User.objects.get(username="jameswatt22")
	martin = User.objects.get(username="martingreg")

	comments = { Recipe.objects.get(name="Chocolate cake"):
					[{"user": james, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : "Pretty plain, but 	very easy to make.I don t think will do it again"}, 
					{"user": sofia, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : "My grandchildren will come tomorrow, now i Know what I am going to do!"}, 
					],

				Recipe.objects.get(name="Chocolate and orange scones"):
					[{"user": james, "date": timezone.now() - datetime.timedelta(days = 2) ,
						"description" : "Great, easy to make if want to impress your friends at a party."}, 
					{"user": maria, "date": timezone.now() - datetime.timedelta(hours = 20) ,
						"description" : "I am going to the Charity Bake Sale in a few days, Cannot wait to make this recipe for the event"}, 
					{"user": martin, "date": timezone.now() - datetime.timedelta(days = 6) ,
						"description" : "The first recipe that I am doing from this website. Delicious!"}, 
					],

				Recipe.objects.get(name="Cherry pie"):
					[{"user": sofia, "date": timezone.now() - datetime.timedelta(minutes = 2) ,
						"description" : "Delicious!"}, 
					{"user": sofia, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : "This recipe is great for summer!"}, 
					],

				Recipe.objects.get(name="Double chocolate cherry brownies"):
					[{"user":martin , "date": timezone.now() - datetime.timedelta(hours= 2) ,
						"description" : "Just finished preparing the brownies. Amazing recipe!"}, 
					{"user": sofia, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : "Take quite some time to make for some brownies..."}, 
					{"user": james, "date": timezone.now() - datetime.timedelta(hours = 6) ,
						"description" : "Thanks for the recipe!"}, 
					],

				Recipe.objects.get(name="Orange butterfly cakes"):
					[{"user": elliot, "date": timezone.now() - datetime.timedelta(days = 1) ,
						"description" : "So aesthetic!"}, 
					{"user": maria, "date": timezone.now() - datetime.timedelta(hours = 20) ,
						"description" : "Tried this at a baking competition... Everyone was impressed"}, 
					{"user": james, "date": timezone.now() - datetime.timedelta(minutes = 30) ,
						"description" : "Nice recipe!"}, 
					],


				Recipe.objects.get(name="Mary’s Victoria sandwich with buttercream"):
					[{"user": elliot, "date": timezone.now() - datetime.timedelta(hours = 22) ,
						"description" : "Very difficult to make, will not recomment this to a beginner!"}, 
					{"user": martin, "date": timezone.now() - datetime.timedelta(minutes = 103) ,
						"description" : "Great if you want to impress someone with your baking skills"}, 
					],

				Recipe.objects.get(name="Apple pie"):
					[{"user": james, "date": timezone.now() - datetime.timedelta(hours = 2) ,
						"description" : "This is recipe for disaster! The way you mix ingredients is tottaly wrong!"}, 
					{"user": maria, "date": timezone.now() - datetime.timedelta(hours = 4) ,
						"description" : "It was decent, doesn't stand out with anything"}, 
					],

				Recipe.objects.get(name="Salted chocolate cake"):
					[{"user": elliot, "date": timezone.now() - datetime.timedelta(days = 2) ,
						"description" : "If you do not try this recipe bc you think it is too plain, please have second thoughts. It is delicious"}, 
					{"user": james, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : " 5 starts for this!"}, 
					{"user": martin, "date": timezone.now() - datetime.timedelta(days = 3) ,
						"description" : "Amazing taste!"}, 
					{"user": maria, "date": timezone.now() - datetime.timedelta(hours = 10) ,
						"description" : "Difficult to make for beginners, but the flavour is so intense!"}
					],

				Recipe.objects.get(name="Mini apple and almond cakes"):
					[{"user": elliot, "date": timezone.now() - datetime.timedelta(hours = 20) ,
						"description" : "Delicous, easy to make! Love your recipes!"}, 
					{"user": sofia, "date": timezone.now() - datetime.timedelta(hours = 19) ,
						"description" : "Thank you elliot!"}, 
					{"user": james, "date": timezone.now() - datetime.timedelta(hours = 10) ,
						"description" : "yummy!"}, 
					{"user": maria, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : "So cuuuute!"},
					{"user": martin, "date": timezone.now() - datetime.timedelta(minutes = 30) ,
						"description" : "Great for a party with friends!:)"}, 
					],

				Recipe.objects.get(name="Chocolate flapjacks"):
					[{"user": elliot, "date": timezone.now() - datetime.timedelta(hours = 20) ,
						"description" : "Healthy stuff for anyone's children"}, 
					{"user": maria, "date": timezone.now() - datetime.timedelta(hours = 19) ,
						"description" : "thank you elliot"}, 
					{"user": sofia, "date": timezone.now() - datetime.timedelta(hours = 10) ,
						"description" : "Delicious!Thanks!"}, 
					{"user": maria, "date": timezone.now() - datetime.timedelta(hours = 9) ,
						"description" : "thank youu!"},
					{"user": james, "date": timezone.now() - datetime.timedelta(minutes = 2) ,
						"description" : "Very yummy"}, 
					{"user": martin, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : "Esay to make, love the taste!"}
					],

				Recipe.objects.get(name="Steamed syrup sponge pudding"):
					[{"user": elliot, "date": timezone.now() - datetime.timedelta(minutes = 10) ,
						"description" : "The recipe looks very interesting, will try it at the charity event"}, 
					{"user": sofia, "date": timezone.now() - datetime.timedelta(minutes = 20) ,
						"description" : "Looks fancy!"}, 
					],

									

	}

	for recipe, all_comments in comments.items():
		for comment_data in all_comments:
			add_comment(comment_data["user"], recipe, comment_data["date"], comment_data["description"])



	# make some users save recipes
	add_saved_recipe(elliot,Recipe.objects.get(name="Steamed syrup sponge pudding"))
	add_saved_recipe(elliot,Recipe.objects.get(name="Apple pie"))
	add_saved_recipe(elliot,Recipe.objects.get(name="Mary’s Victoria sandwich with buttercream"))
	add_saved_recipe(elliot,Recipe.objects.get(name="Carrot cake loaf"))
	add_saved_recipe(elliot,Recipe.objects.get(name="Chocolate flapjacks"))
	add_saved_recipe(elliot,Recipe.objects.get(name= "Lemon and almond cake"))

	add_saved_recipe(sofia, Recipe.objects.get(name="Chocolate flapjacks"))
	add_saved_recipe(sofia, Recipe.objects.get(name="Lemon and almond cake"))
	add_saved_recipe(sofia, Recipe.objects.get(name="Chocolate cake"))
	add_saved_recipe(sofia, Recipe.objects.get(name="Chocolate and orange scones"))

	add_saved_recipe(maria,Recipe.objects.get(name="Apple pie"))
	add_saved_recipe(maria,Recipe.objects.get(name="Chocolate cake"))
	add_saved_recipe(maria,Recipe.objects.get(name="Steamed syrup sponge pudding"))
	add_saved_recipe(maria,Recipe.objects.get(name="Lemon and almond cake"))
	add_saved_recipe(maria,Recipe.objects.get(name="Chocolate and orange scones"))


	add_saved_recipe(james,Recipe.objects.get(name="Apple pie"))


if __name__ == '__main__':
    print("Starting Sweetbook population script...")
    populate()

