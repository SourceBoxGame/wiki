# Lua Objects

Objects store a number of variables and functions which are defined in the class the object comes from. They kind of act like tables but are not modifiable. Meaning, if you wanted to make a new variable or function inside an object, you would get an error.

Another thing that is different from tables is that you cannot change the type of the variables. Once they have been defined, that's it. You cannot change that variable to any other type which it originally was defined with.

To create a new object, simply call the `object()` function with a class, and it will return a new object based on the class you gave it.

    my_class = class() -- Start creating the class

    my_class.var = 10.0 -- Make a variable

    finish(my_class) -- Finish the class

    my_object = object(my_class) -- Make the object

---

[<- Prev][QScript/Lua/Classes] |
[Next ->][QScript/Lua/Exports]