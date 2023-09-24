# Squirrel Exports and Imports

The main big feature of QScript is the export system. It lets you export classes, objects and functions which other files can import from your script.

Let's say that you have a library called "MyLib.nut" inside a mod called "MyMod". This is what it contains:

MyMod/MyLib.nut
    class AdditionClass
    {
        function Add(a,b)
        {
            return a + b;
        }
    }

    Addition <- AdditionClass() -- Exports can only use global variables!

Now to export the `Addition` object, pass them to the `export()` function at the end of the file.

MyMod/MyLib.nut
    export(Addition);

To import the exported elements in another file, simply use the `import()` function with the file path of the script you want to import from.

    MyLib <- import("MyMod/MyLib.nut");

    MyLib.Addition.Add(2,5); -- will return 7

---

[<- Prev][QScript/Squirrel/Intro] |
[Go back to the QScript Tutorial][QScript/Tutorial/Chapter1]