# Lua Exports

Here is the real meat and potatoes of QScript. The import/export system allows you to share objects, functions and classes between scripts and other languages! The system is stupidly simple to understand.

Here is a simple code example:

    function Add(a,b)
        return a + b
    end

    export(Add)

That is it! Just put the global variable you want to export in the global scope (not inside another function) and the thing you want to export will get added to a special list which will contain all the exported elements from your file.

Exporting classes and objects works the same way.

    my_class = class()

    finish(my_class)

    my_object = object(my_class)

    export(my_class)
    export(my_object)

That's great but now what can you do with the exported variables? That's the thing. You don't! Other scripts use the exported variables. See how and why in the next page.

---

[<- Prev][QScript/Lua/Objects] |
[Next ->][QScript/Lua/Imports]