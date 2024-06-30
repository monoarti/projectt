import random
from tkinter import *
from tkinter.ttk import *
import directions


class Recipe:
    def __init__(self, name, ingredients, meal):
        self.name = name
        self.ingredients = ingredients
        self.meal = meal



class MealPlan:
    def __init__(self):
        self.meals = {
            "breakfast" : random.choice(breakfast_meals),
            "lunch" : random.choice(lunch_or_dinner_meals),
            "dinner" : random.choice(lunch_or_dinner_meals)
        }


recipes = [
    Recipe("pancake", {"egg":2, "milk":1/4, "flour":1/4, "honey":2, "butter":1, "vanilla":1}, "breakfast"),
    Recipe("french toast", {"milk":1/2, "egg":3, "honey":2, "butter":2, "bread":4}, "lunch/dinner"), 
    Recipe("garlic bread", {"butter":2, "garlic":2, "cheese":2, "bread":4}, "lunch/dinner"),
    Recipe("snack eggs", {"egg":2, "bread":2, "ketchup":1}, "breakfast"), 
    Recipe("rice", {"rice":1, "butter":1}, "lunch/dinner"),
    Recipe("waffles", {"flour":11/2, "baking powder":3, "sugar":1/2, "milk":3/2, "egg":2, "butter":3, "vanilla":1/2}, "breakfast"),
    Recipe("chicken teriaki", {"soy sauce":3/4, "mayonnaise":1, "checken":1}, "lunch/dinner")
]

breakfast_meals = [recipe for recipe in recipes if recipe.meal == "breakfast"]
lunch_or_dinner_meals = [recipe for recipe in recipes if recipe.meal == "lunch/dinner"]


refrigerator = {
    "egg" : 0,
    "milk" : 0,
    "bread" : 4,
    "tomato" : 0,
    "cheese" : 2,
    "rice" : 1, 
    "butter" : 2,
    "garlic" : 2
    }


def suggest_recipe():
    available_ingredients = refrigerator.keys()
    suggested_recipes = []
    for recipe in recipes:
        if all(ingredient in available_ingredients for ingredient in recipe.ingredients) and\
        all(refrigerator[ingredient] >= recipe.ingredients[ingredient] for ingredient in recipe.ingredients):
            suggested_recipes.append(recipe)
    return suggested_recipes
        

def generate_shopping_list(meal_plan):
    shopping_list = {}
    ingredients = {}
    for meal in meal_plan.meals.values():
        for ingredient , amount in meal.ingredients.items():
            try:
                ingredients[ingredient] += amount
            except KeyError:
                ingredients[ingredient] = amount
    for ingredientt , amountt in ingredients.items():
        if ingredientt not in refrigerator or amountt > refrigerator[ingredientt]:
                shopping_list[ingredientt] = amountt
    return shopping_list

            


def main():
    root = Tk()
    root.title('Refrigerator Menu')
    root.geometry("750x550")
    menubar = Menu(root)

    def clear(): # to clear all widgets and refresh the root
        listt = root.pack_slaves()
        for l in listt:
            l.destroy()

    def add_recipe_gui():
        clear()
        r_str = StringVar()
        r_str.set("lunch/dinner")
        button_frame = Frame(root).pack()
        l1 = Label(root, text= "Enter recipe name: ").pack()
        E1 = Entry(root)
        E1.pack()
        R1 = Radiobutton(root, text="breakfast", variable=r_str, value="breakfast").pack()
        R2 = Radiobutton(root, text="lunch/dinner", variable=r_str, value="lunch/dinner").pack()
        l2 = Label(root, text= "Write ingredients and their amounts in each line: (before amount plz enter a space)").pack()
        T1 = Text(root)
        T1.pack()
        B1 = Button(root, text="click if done", command=lambda: done1(E1, r_str, T1)).pack()
        def done1(E, R, T):
            name = E.get().lower()
            meal = R.get()
            ingredients = set(T.get(1.0, END).split("\n")) # to remove duplicates in ingredients
            # to remove spaces in text entry
            ingredients.discard("") 
            ingredients.discard(" ")
            # to seprate an ingredient from its amount
            dictt = {}
            for item in ingredients:
                listt = []
                for word in item.split(" "):
                    try:
                        amount = float(word)
                    except ValueError:
                        listt.append(word)
                ingredient = " ".join(listt)
                dictt[ingredient.lower()] = amount
            # add the new recipe to the recipes list
            recipes.append(Recipe(name, dictt, meal))
            # add the directons of this meal to the recipe_direction dictionary
            clear()
            l = Label(root, text="Write the directions of this meal: ").pack()
            t = Text(root)
            t.pack()
            B2 = Button(root, text="click if done", command=lambda: done2(t)).pack()
            def done2 (t): 
                direction = t.get(1.0, END)
                directions.recipe_directions[name] = direction
                clear()
                l = Label(root, text="It is successfully done. Thank You!").pack()

    def suggest_recipe_gui():
        clear()
        suggested_recipes = suggest_recipe()
        n = "\n"
        if len(suggested_recipes) == 0:
            l1 = Label(root, text="Sorry, no matching recipes found.").pack()
        else:
            for recipe in suggested_recipes:
                l2 = Label(root, text=f"Suggested recipe : {recipe.name}{n}It can be made for {recipe.meal}{n}The recipe directions :{n} {directions.recipe_directions[recipe.name]}").pack()
                line = Label(root, text="_____________________________________").pack()

    def shopping_list_gui():
        clear()
        meal_plan = MealPlan()
        shopping_list = generate_shopping_list(meal_plan)
        l1 = Label(root, text="Your meal plan for today is: ").pack()
        l2 = Label(root, text=f"breakfast : {meal_plan.meals['breakfast'].name}").pack()
        l3 = Label(root, text=f"lunch : {meal_plan.meals['lunch'].name}").pack()
        l4 = Label(root, text=f"dinner : {meal_plan.meals['dinner'].name}").pack()
        line = Label(root, text="_____________________________________").pack()
        l5 = Label(root, text="Shopping List:").pack()
        for ingredient, amount in shopping_list.items():
            l = Label(root, text=f"{ingredient}: {amount} units").pack()

    def doing_the_shopping_gui():
        clear()
        l1 = Label(root, text= "Write ingredients and their amounts you,ve bought in each line: (before amount plz enter a space)").pack()
        t = Text(root)
        t.pack()
        B1 = Button(root, text="click if done", command=lambda: done(t)).pack()
        def done(t):
            ingredients = set(t.get(1.0, END).split("\n")) # to remove duplicates in ingredients
            # to remove spaces in text entry
            ingredients.discard("") 
            ingredients.discard(" ")
            # to seprate an ingredient from its amount
            for item in ingredients:
                listt = []
                for word in item.split(" "):
                    try:
                        amount = float(word)
                    except ValueError:
                        listt.append(word)
                ingredient = " ".join(listt)
                try:
                    refrigerator[ingredient] += amount
                except KeyError:
                    refrigerator[ingredient] = amount
            clear()
            l = Label(root, text="It is successfully done. Thank You!").pack()

    def cooking_a_meal_gui():
        clear()
        l1 = Label(root, text="Enter the meal name you want to cook: ")
        l1.pack()
        E = Entry(root)
        E.pack()
        B = Button(root, text="click if done", command=lambda: done(E)).pack()
        def done(E):
            name = E.get()
            clear()
            flag = False
            for recipe in recipes:
                if recipe.name == name:
                    for ingredient , amount in recipe.ingredients.items():
                        if ingredient not in refrigerator or amount > refrigerator[ingredient]:
                            l = Label(root, text=f"Sorry! you can't cook this for the lack of {ingredient}").pack()
                            flag = True
                    if all(ingredient in refrigerator.keys() for ingredient in recipe.ingredients) and\
                    all(refrigerator[ingredient] >= recipe.ingredients[ingredient] for ingredient in recipe.ingredients):
                        l1 = Label(root, text=f"The recipe directions : {directions.recipe_directions[recipe.name]}").pack()
                        l2 = Label(root, text="Have a good cooking time:)").pack()
                        for ingredient , amount in recipe.ingredients.items():
                            refrigerator[ingredient.lower()] -= amount
                        flag = True
                        print(refrigerator)
            if flag == False: # the meal name you entered not found in recipes 
                l = Label(root, text="Sorry! I don't know the recipe of this meal:(").pack()
                

    menubar.add_command(label="Add Recipe", command=add_recipe_gui)
    menubar.add_command(label="Suggest Recipe", command=suggest_recipe_gui)
    menubar.add_command(label="Shopping list", command=shopping_list_gui)
    menubar.add_command(label="Doing a shopping", command=doing_the_shopping_gui)
    menubar.add_command(label="Cooking a meal", command=cooking_a_meal_gui)

    root.config(menu=menubar)
    root.mainloop()




if __name__=="__main__":
    main()
