# QScript Rundown Page 5

Scripting language interfaces inherit from [[IBaseScriptingInterface]]. While there is not one way of implementing the interface, it is best to learn how each one works. Let's start with Lua.

When the game starts up, it will initialize all DLLs. During initialization, it will call the `Connect()` function which you use to connect to other DLLs. Lua connects to tier1, filesystem, and qscript itself. It also sets the `current_interface` variable to `this`.

$_SMALL luainterface/luainterface.cpp _$
```cpp
bool CLuaInterface::Connect(CreateInterfaceFn factory)
{
    ConnectTier1Libraries(&factory, 1);
    ConVar_Register();
    g_pFullFileSystem = (IFileSystem*)factory(FILESYSTEM_INTERFACE_VERSION, NULL);
    g_pQScript = (IQScript*)factory(QSCRIPT_INTERFACE_VERSION, NULL);
    current_interface = this;
    return true;
}
```

You are expected to return `true` if nothing went wrong during connection.

After that, other DLLs will call to QScript add their modules. That happens during the `Init()` phase.
After each module is loaded (at `PostInit()`), QScript will call `ImportModules()` with the modules `CUtlVector<QModule*>*` you can safely save it to the interface object if you dont want to do anything during import.

$_SMALL luainterface/luainterface.cpp _$
```cpp
void CLuaInterface::ImportModules(CUtlVector<QModule*>* modules)
{
    m_modules = modules;
}
```

After that, there come the mods. QScript will just give you the file path of the mod along with the [[QMod]] itself. You must check whether the extension matches your scripting language. If it does not, return 0, but if it does, load the file yourself and return a [[QInstance]] pointer.

This is where things start getting complicated.

---

$_FRAME
[<- Prev][QScriptRundown4] | [Next ->][QScriptRundown6]
_$