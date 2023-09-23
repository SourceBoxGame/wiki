# Lua Classes

If you want to create a class, you first call the `class()` function like this:


    my_class = class() -- Creates a class creator


`my_class` becomes a class creator. You can think of it like a bowl of ingredients which you can add to by simply setting the values of it.


    my_class = class() -- Creates a class creator

    my_class.MyVar = 50.0 -- Creates a variable inside the class
    function my_class.MyFunc(self,a) -- Creates a function inside the class
        return self.MyVar+a
    end


Once you are done with defining your class, you call the `finish()` function like this:


    finish(my_class) -- Finishes the class


`my_class` will turn into a normal class where you cannot add any more variables or functions to it. In other words, `my_class` will get "baked" and you cannot add any more ingredients to it.

---

[Next ->][QScript/Lua/Objects]