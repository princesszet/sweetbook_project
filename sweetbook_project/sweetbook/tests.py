from django.test import TestCase

#def
test_slug_line_creation(self):
"""
slug_line_creation checks to make sure that when we add
a category an appropriate slug line is created
i.e. "Random Category String" -> "random-category-string"
"""
recipe=recipe'Random Category String')
recipe.save()
self.assertEqual(recipe.slug,'random-category-string')
