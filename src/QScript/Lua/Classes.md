# Lua Classes

Let's start with an analogy. Imagine you want to make star-shaped cookies. You could of course, manually cut the baked cookie and then be left with a mess, or you could use a cookie cutter before baking it. In this analogy, the cookie is an object, the manual cutting method is using tables, and the cookie cutter is a class.

Before explaining what an object is, let's first take a look at how you even make a class.

To create a class, you first call the `class()` function like this:

```lua
my_class = class() -- Creates a class creator
```

`my_class` becomes a class creator. You can think of it like a bowl of ingredients which you can add to by simply setting the values of it.

```lua
my_class = class() -- Creates a class creator

my_class.MyVar = 50.0 -- Creates a variable inside the class
function my_class.MyFunc(self,a) -- Creates a function inside the class
    return self.MyVar+a
end
```

Once you are done with defining your class, you call the `finish()` function like this:

```lua
finish(my_class) -- Finishes the class
```

`my_class` will turn into a normal class where you cannot add any more variables or functions to it. In other words, `my_class` will get "baked" and you cannot add any more ingredients to it.

The `class()` function accepts another class as a parameter which will "inherit" the other class.

In simple terms, every function and variable from the other class, will be copied into yours, without having to specify them all over again.

    another_class = class(my_class) -- Inherits from my_class

    another_class.MyVar = 20.0 -- Changes the existing variable
    function another_class.NewFunc(self,b) -- Makes a new function
        return self.MyVar-b
    end

    finish(another_class) -- Finishes it

We can now move on to objects.

---

[<- Prev][QScript/Lua/Intro] |
[Next ->][QScript/Lua/Objects]