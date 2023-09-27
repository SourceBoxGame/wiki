# QScript Rundown Page 6

In Lua, the `ExecuteLua()` function does what it says. It executes a Lua script, while it may sound simple, a lot comes into that.

I figured that it may be easiest to just go through the function seciton by section.

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
lua_State* L = luaL_newstate();
```
---
Simply create a new lua state.
_$

<br />

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
QInstance* ins = new QInstance();
ins->env = L;
ins->lang = (IBaseScriptingInterface*)current_interface;
```
---
Create a new QInstance which contains the current language interface and Lua instance
_$

<br />

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
luaL_openlibs(L);
```

---

Which is:

$_INLINEFRAME
$_SMALL lua/linit.c _$
```c
static const luaL_Reg loadedlibs[] = {
  {LUA_GNAME, luaopen_base},
  {LUA_COLIBNAME, luaopen_coroutine},
  {LUA_TABLIBNAME, luaopen_table},
  {LUA_STRLIBNAME, luaopen_string},
  {LUA_MATHLIBNAME, luaopen_math},
  {LUA_UTF8LIBNAME, luaopen_utf8},
  {NULL, NULL}
};


LUALIB_API void luaL_openlibs (lua_State *L) {
  const luaL_Reg *lib;
  /* "require" functions from 'loadedlibs' and set results to global table */
  for (lib = loadedlibs; lib->func; lib++) {
    luaL_requiref(L, lib->name, lib->func, 1);
    lua_pop(L, 1);  /* remove lib */
  }
}
```

---

You can notice that it does not include every library, thats because QScript values safety and stability. Some libraries allow for bad things to happen, like unrestricted file access.

_$

_$

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
luaL_newmetatable(L, "QSCRIPT_OBJECT");
lua_pushstring(L, "__index");
lua_pushcclosure(L, Lua_QScript_Index, 0);
lua_settable(L, -3);
```

---

Here the QSCRIPT_OBJECT metatable starts being defined and here is where things start to get a little wild.
The Lua_QScript_Index function is responsible for getting a value or method from the QObject.

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Index(lua_State* L)
{
    QObject* obj;
    Lua_Userdata* usr;
    if (!(usr = (Lua_Userdata*)luaL_checkudata(L, 1, "QSCRIPT_OBJECT")))
        return 0;
    obj = usr->obj;
    const char* name = lua_tostring(L, 2);
    int index = g_pQScript->GetObjectValueIndex((QScriptObject)obj, name);
    if (index == -1)
    {
        index = g_pQScript->GetObjectMethodIndex((QScriptObject)obj, name);
        if (index == -1)
            return 0;
        QFunction* func = (QFunction*)g_pQScript->GetObjectMethod((QScriptObject)obj, index);
        usr = (Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata));
        usr->func = func;
        luaL_setmetatable(L, "QSCRIPT_FUNCTION");
        return 1;
    }
    QValue val = g_pQScript->GetObjectValue((QScriptObject)obj, index);
    QType type = g_pQScript->GetObjectValueType((QScriptObject)obj, index);
    switch (type)
    {
    case QType_Int:
        lua_pushinteger(L, val.value_int);
        return 1;
    case QType_String:
        lua_pushstring(L, val.value_string);
        return 1;
    case QType_Float:
        lua_pushnumber(L, val.value_float);
        return 1;
    case QType_Bool:
        lua_pushboolean(L, val.value_bool);
        return 1;
    default:
        lua_pushnil(L);
        return 1;
    }
}
```

---

You can notice that this is just a regular Lua C function. And the way it is pushed to the Lua stack suggests so... You will see why im pointing this out later.
The function itself first checks the userdata and gets the wanted value name from the second argument.
It searches first through the values, and then the methods. If any one is found, the appropriate conversion is performed.

Something interesting that happens here is this snippet:

$_SMALL luainterface/luainterface.cpp _$
```cpp
QFunction* func = (QFunction*)g_pQScript->GetObjectMethod((QScriptObject)obj, index);
usr = (Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata));
usr->func = func;
luaL_setmetatable(L, "QSCRIPT_FUNCTION");
```


You can notice it creating a Lua_Userdata struct with the userdata, why is that?

The Lua_Userdata is more of a union pointer than a struct, this is the definition of it:

$_SMALL luainterface/luainterface.cpp _$
```cpp
struct Lua_Userdata
{
    union {
        QObject* obj;
        QClass* cls;
        QClassCreator* creator;
        QFunction* func;
    };
};
```

You can notice that it can store multiple types, and there is not even a separate variable that says which one it is!
The reason, is that we already have that variable... it's the metatable!

We already know if the userdata has a specific metatable, that the pointer stored in the userdata is what we want.

_$

_$

<br />
In fact, here are all the Lua functions that get included.
<br />
<hr />
<br />

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_New_Index(lua_State* L)
{
    QObject* obj;
    Lua_Userdata* usr;
    if (!(usr = (Lua_Userdata*)luaL_checkudata(L, 1, "QSCRIPT_OBJECT")))
        return 0;
    obj = usr->obj;
    const char* name = lua_tostring(L, 2);
    int index = g_pQScript->GetObjectValueIndex((QScriptObject)obj, name);
    if (index == -1)
        return 0;
    QType type = g_pQScript->GetObjectValueType((QScriptObject)obj, index);
    QValue val;
    switch (type) // TODO : error check the type
    {
    case QType_Int:
        val.value_int = lua_tointeger(L, 3);
        g_pQScript->SetObjectValue((QScriptObject)obj, index, val);
        return 0;
    case QType_String:
        g_pQScript->SetObjectString((QScriptObject)obj, index, lua_tostring(L,3));
        return 0;
    case QType_Float:
        val.value_float = lua_tonumber(L, 3);
        g_pQScript->SetObjectValue((QScriptObject)obj, index, val);
        return 0;
    case QType_Bool:
        val.value_bool = lua_toboolean(L, 3);
        g_pQScript->SetObjectValue((QScriptObject)obj, index, val);
        return 0;
    default:
        return 0;
    }
}
```

_$