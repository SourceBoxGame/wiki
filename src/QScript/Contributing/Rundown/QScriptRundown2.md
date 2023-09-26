# QScript Rundown Page 2

If you want to add a feature to QScript, you first have to decide what layer it should lie in. If you want to add a new entity to QScript, you just modify the top-level game layer. If you want to add a new scripting functionality, you might want to modify QScript and the interfaces, but if you want to add something to a scripting language, you must modify its source code directly.

An example of modifying a scripting language is what had to be done with Squirrel.

Squirrel does not support inheriting from userdata, so what had to be done is to modify the source code of it to make it possible.
Same thing with changing the class after it has been created. I have added a _finish metamethod which gets called when the class is finished defining its methods. Its return value is what the class will be set to at the end.

The fact that you can inherit from a userdata, and then get another userdata instance should not be possible in regular Squirrel. This is an example of modifying the scripting language to fit our needs.

[<- Prev][QScriptRundown1.md] | [Next ->][QScriptRundown3.md]