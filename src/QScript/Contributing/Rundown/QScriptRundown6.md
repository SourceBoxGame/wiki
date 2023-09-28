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

---

This sets a value in the QObject. It checks if the value accessed actually exists in the object, and if so, sets the objects value to the given one.

_$
<br />
$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Object(lua_State* L)
{
    Lua_Userdata* luaclass;
    if(!(luaclass = (Lua_Userdata*)luaL_checkudata(L,1,"QSCRIPT_CLASS")))
        return 0;
    QClass* cls = luaclass->cls;
    QObject* obj = (QObject*)malloc(sizeof(QObject)+cls->vars_count*sizeof(QValue));
    obj->cls = cls;
    g_pQScript->InitializeObject((QScriptObject)obj);
    ((Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata)))->obj = obj;
    luaL_setmetatable(L, "QSCRIPT_OBJECT");
    return 1;
}
```

---

`object()` createa a new object from the passed class. It initializes it and returns it to Lua.

_$
<br />
$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Class(lua_State* L)
{
    Lua_Userdata* parentluaclass;
    QClass* cls = 0;
    if (lua_gettop(L) == 0)
        return 0; // TODO : error here
    if (lua_gettop(L) > 0)
    {
        if (!(parentluaclass = (Lua_Userdata*)luaL_checkudata(L, 1, "QSCRIPT_CLASS")))
            return 0; // TODO : error here
        cls = parentluaclass->cls;
    }
    Lua_Userdata* luaclass = (Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata));
    luaclass->creator = new QClassCreator();
    QClassCreator* child = luaclass->creator;
    child->parent = cls;
    child->name = 0;
    luaL_setmetatable(L, "QSCRIPT_CLASS_CREATOR");
    return 1;
}
```

---

`class()` creates a new class creator. It takes an optional class as the parent class and returns a new QClassCreator struct.

_$
<br />
$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Class_Creator_NewIndex(lua_State* L)
{
    Lua_Userdata* luaclass;
    if (!(luaclass = (Lua_Userdata*)luaL_checkudata(L, 1, "QSCRIPT_CLASS_CREATOR")))
        return 0; // TODO : error here
    QClassCreator* cls = luaclass->creator;
    if (lua_isfunction(L, 3))
    {
        QClassCreatorMethod* meth = (QClassCreatorMethod*)lua_newuserdata(L, sizeof(QClassCreatorMethod));
        lua_pushvalue(L, 3);
        QCallback* callback = new QCallback();
        callback->callback = (void*)luaL_ref(L, LUA_REGISTRYINDEX);
        callback->lang = current_interface;
        callback->env = L;
        callback->object = 0;
        meth->scripting_func = callback;
        meth->is_scripting = true;
        const char* name = lua_tostring(L, 2);
        meth->name = new char[strlen(name)+1];
        strcpy(const_cast<char*>(meth->name), name);
        meth->is_private = false;
        meth->params = 0;
        meth->params_count = 0;
        cls->methods.AddToTail(meth);
        lua_pop(L, 1);
        return 0;
    }
    else
    {
        QVar* var = new QVar();
        var->is_private = false;
        const char* name = lua_tostring(L, 2);
        var->name = new char[strlen(name)+1];
        strcpy(const_cast<char*>(var->name), name);
        if (lua_isstring(L, -1))
        {
            var->type = QType_String;
            const char* str = lua_tolstring(L, 3, 0);
            var->size = 1<<Qlog2(strlen(str));
            var->defaultval.value_modifiable_string = (char*)malloc(var->size+1);
            strcpy(var->defaultval.value_modifiable_string, str);
        }
        else if (lua_isinteger(L, -1))
        {
            var->type = QType_Int;
            var->defaultval.value_int = lua_tointeger(L, 3);
        }
        else if (lua_isnumber(L, -1))
        {
            var->type = QType_Float;
            var->defaultval.value_float = lua_tonumber(L, 3);
        }
        else if (lua_isboolean(L, -1))
        {
            var->type = QType_Bool;
            var->defaultval.value_bool = (bool)lua_toboolean(L, 3);
        }
        else
        {
            var->type = QType_None;
        }
        cls->vars.AddToTail(var);
        return 0;
    }
}
```

---

Creates a variable or function in the `QClassCreator` struct.

_$
<br />
$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Finish(lua_State* L)
{
    Lua_Userdata* luaclass;
    if (!(luaclass = (Lua_Userdata*)luaL_checkudata(L, 1, "QSCRIPT_CLASS_CREATOR")))
        return 0; // TODO : error here
    QClassCreator* cls = luaclass->creator;
    luaclass->cls = (QClass*)g_pQScript->FinishClass((QScriptClassCreator)cls);
    luaL_setmetatable(L, "QSCRIPT_CLASS");
    return 0;
}
```

---

{{Stub}}

_$
<br />
$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Export(lua_State* L)
{
    lua_Debug dbg;
    if (lua_getstack(L, 2, &dbg))
        return 0; // TODO : error here, function can only be executed in global context
    QInstance* ins = (QInstance*)lua_touserdata(L,lua_upvalueindex(1));
    QFunction* func;
    Lua_Userdata* usr;
    if (usr = (Lua_Userdata*)luaL_testudata(L, 1, "QSCRIPT_OBJECT"))
    {
        lua_pushglobaltable(L);
        lua_pushnil(L);
        while (lua_next(L,-2) != 0)
        { 
            if (lua_isuserdata(L, -1) && (usr == (Lua_Userdata*)luaL_testudata(L, -1, "QSCRIPT_OBJECT")))
            {
                QExport* exp = new QExport();
                exp->obj = usr->obj;
                exp->type = QExport_Object;
                exp->name = lua_tostring(L, -2);
                ins->exports.AddToTail(exp);
                lua_pop(L, 3);
                return 0;
            }
            lua_pop(L, 1);
        }
        // TODO : error here, must be a global variable
        return 0;
    }
    else if (usr = (Lua_Userdata*)luaL_testudata(L, 1, "QSCRIPT_CLASS"))
    {
        lua_pushglobaltable(L);
        lua_pushnil(L);
        while (lua_next(L, -2) != 0)
        {
            if (lua_isuserdata(L, -1) && (usr == (Lua_Userdata*)luaL_testudata(L, -1, "QSCRIPT_CLASS")))
            {
                QExport* exp = new QExport();
                exp->cls = usr->cls;
                exp->type = QExport_Class;
                exp->name = lua_tostring(L, -2);
                ins->exports.AddToTail(exp);
                lua_pop(L, 3);
                return 0;
            }
            lua_pop(L, 1);
        }
        // TODO : error here, must be a global variable
        return 0;
    }
    else if (lua_isfunction(L,1))
    {
        lua_pushglobaltable(L);
        lua_pushnil(L);
        while (lua_next(L, -2) != 0)
        {
            if (lua_isfunction(L, -1) && lua_rawequal(L, -1, 1))
            {
                func = new QFunction();
                func->always_zero = 0;
                func->type = QFunction_Scripting;
                QCallback* callback = new QCallback();
                lua_pushvalue(L, 1);
                callback->callback = (void*)luaL_ref(L, LUA_REGISTRYINDEX);
                callback->env = L;
                callback->lang = current_interface;
                callback->object = 0;
                func->func_scripting = callback;
                QExport* exp = new QExport();
                exp->func = func;
                exp->type = QExport_Function;
                exp->name = lua_tostring(L, -2);
                ins->exports.AddToTail(exp);
                lua_pop(L, 3);
                return 0;
            }
            lua_pop(L, 1);
        }
        // TODO : error here, must be a global variable
        return 0;
    }
    // TODO : error here, must be a QObject, QClass or QFunction
    return 0;
}
```

---

{{Stub}}

_$
<br />
$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Import(lua_State* L)
{
    lua_Debug dbg;
    if (lua_getstack(L, 2, &dbg))
        return 0; // TODO : error here, function can only be executed in global context
    QMod* mod = (QMod*)lua_touserdata(L, lua_upvalueindex(1));
    const char* path;
    if (!(path = luaL_checkstring(L, 1)))
        return 0; // TODO : error here, string is required
    if (!IsValidPath(path))
        return 0; // TODO : error here, nuh uh
    if (!mod->instances.Defined(path))
    {
        mod->instances[path] = 0;
        g_pQScript->LoadFile(path);
    }
    QInstance* inst = mod->instances[path];
    if (!inst)
        return 0; // TODO : error here, most likely a import loop or bad path
    CUtlVector<QExport*>* exports = &mod->instances[path]->exports;
    Lua_Userdata* ud;
    lua_createtable(L, 0, exports->Count());
    for (int i = 0; i < exports->Count(); i++)
    {
        QExport* qexport = exports->Element(i);
        lua_pushstring(L, qexport->name);
        switch (qexport->type)
        {
        case QExport_Object:
            ud = (Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata));
            ud->obj = qexport->obj;
            luaL_setmetatable(L, "QSCRIPT_OBJECT");
            break;
        case QExport_Class:
            ud = (Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata));
            ud->cls = qexport->cls;
            luaL_setmetatable(L, "QSCRIPT_CLASS");
            break;
        case QExport_Function:
            ud = (Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata));
            ud->func = qexport->func;
            luaL_setmetatable(L, "QSCRIPT_FUNCTION");
            break;
        }
        lua_settable(L, -3);
    }
    return 1;
}
```

---

{{Stub}}

_$
<br />
$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp
int Lua_QScript_Function_Call(lua_State* L)
{
    Lua_Userdata* usr = (Lua_Userdata*)luaL_checkudata(L,1,"QSCRIPT_FUNCTION");
    if (!usr)
        return 0;
    QFunction* func = usr->func;
    if (func->always_zero)
        return 0;
    QArgs* args;
    QReturn ret;
    lua_remove(L, 1);
    int count = lua_gettop(L);
    switch (func->type)
    {
    case QFunction_Module:
        return LuaActualCallback(L, func);
    case QFunction_Native:
        Warning("Calling QFunction_Native is unsuppported in Lua yet (you can add it if you want at line %i in file luainterface.cpp)\n", __LINE__);
        return 0;
    case QFunction_Scripting:
        args = (QArgs*)malloc(count * sizeof(QArg) + sizeof(QArgs));
        args->count = count;
        args->self = 0;
        for (int i = 0; i < count; i++)
        {
            Lua_Userdata* nusr;
            union QValue val;
            if (lua_isinteger(L, i + 1))
            {
                args->args[i].type = QType_Int;
                val.value_int = lua_tointeger(L, i + 1);
            }
            else if (lua_isnumber(L, i + 1))
            {
                args->args[i].type = QType_Float;
                val.value_float = (float)lua_tonumber(L, i + 1);
            }
            else if (lua_isboolean(L, i + 1))
            {
                args->args[i].type = QType_Bool;
                val.value_bool = lua_toboolean(L, i + 1);
            }
            else if (lua_isstring(L, i + 1))
            {
                args->args[i].type = QType_String;
                val.value_string = lua_tolstring(L, i + 1, 0);
            }
            else if (lua_isfunction(L, i + 1))
            {
                args->args[i].type = QType_Function;
                QCallback* callback = (QCallback*)malloc(sizeof(QCallback));
                lua_pushvalue(L, i + 1);
                callback->callback = (void*)luaL_ref(L, LUA_REGISTRYINDEX);
                callback->lang = current_interface;
                callback->env = L;
                QFunction* func = (QFunction*)malloc(sizeof(QFunction));
                func->always_zero = 0;
                func->func_scripting = callback;
                func->type = QFunction_Scripting;
                val.value_function = (QScriptFunction)func;
            }
            else if (nusr = (Lua_Userdata*)luaL_testudata(L, i + 1, "QSCRIPT_OBJECT"))
            {
                args->args[i].type = QType_Object;
                val.value_object = (QScriptObject)nusr->obj;
            }
            args->args[i].val = val;
            continue;
        }
        QReturn ret = ((IBaseScriptingInterface*)func->func_scripting->lang)->CallCallback(func->func_scripting, args);
        switch (ret.type)
        {
        case QType_Bool:
            lua_pushboolean(L, ret.value.value_bool);
            return 1;
        case QType_Float:
            lua_pushnumber(L, ret.value.value_float);
            return 1;
        case QType_String:
            lua_pushstring(L, ret.value.value_string);
            return 1;
        case QType_Int:
            lua_pushinteger(L, ret.value.value_int);
            return 1;
        case QType_Object:
            ((Lua_Userdata*)lua_newuserdata(L, sizeof(Lua_Userdata)))->obj = (QObject*)ret.value.value_object;
            luaL_setmetatable(L, "QSCRIPT_OBJECT");
            return 1;
        default:
            return 0;
        }
    case QFunction_Void:
        return 0;
    }
    return 0;
}
```

---

{{Stub}}

_$


$_COMMENT

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp

```

---

{{Stub}}

_$

$_INLINEFRAME
$_SMALL luainterface/luainterface.cpp _$

```cpp

```

---

{{Stub}}

_$

_$