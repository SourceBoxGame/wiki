# Lua Imports

Now that you have exported some variables, something's gotta import them! As always, it is very simple to do.

Let's say that you have made a file called "MyLib.lua" inside a mod called "MyMod". These are the contents of it:


MyMod/MyLib.lua
```lua
function add(a,b)
    return a + b
end

export(add)
```

Now you want to import it inside another file. You call the `import()` function with the file name of the thing you want to import. It will return a table containing all the exported variables.

```lua
MyLib = import("MyMod/MyLib.lua") -- Import the library

MyLib.add(5,7) -- Will return 12
```

Importing works between other languages. So you don't need to worry about a library being written in a different language than you would like. (You could even use multiple languages in one project! Think about that!)

The reason why you can't use tables, is because objects, are actually shared! One script can modify it (like set a variable), and every other script will also see the change. Tables differ between languages, meaning that having to manually sync them between eachother would be a bad idea. Here, you only get a "reference" to the object. Meaning that every script sees the *same* object, not copies of it.

---

[<- Prev][QScript/Lua/Exports] |
[Go back to the QScript Tutorial][QScript/Tutorial/Chapter1]