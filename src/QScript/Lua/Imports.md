# Lua Imports

Now that you have exported some variables, something's gotta import them! As always, it is very simple to do.

Let's say that you have made a file called "MyLib.lua" inside a mod called "MyMod". These are the contents of it:

    -- MyMod/MyLib.lua
    function add(a,b)
        return a + b
    end

    export(add)

Now you want to import it inside another file. You call the `import()` function with the file name of the thing you want to import. It will return a table containing all the exported variables.

    MyLib = import("MyMod/MyLib.lua") -- Import the library

    MyLib.add(5,7) -- Will return 12

Importing works between other languages. So you don't need to worry about a library being written in a different language than you would like. (You could even use multiple languages in one project! Think about that!)

---

[<- Prev][QScript/Lua/Exports]