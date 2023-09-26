# QScript API

---

## CreateModule

```cpp
QScriptModule CreateModule(const char* name, QModuleDefFunc* funcs)
```

Takes a name, and a [[QModuleDefFunc]] list, returns a QScriptModule

---

## LoadMods

```cpp
void LoadMods(const char* filename)
```

Will load a file inside the root of every mod.

---

## LoadModsInDirectory

```cpp
void LoadModsInDirectory(const char* folder, const char* filename)
```

Acts like LoadMods, but loads a file inside a subdirectory. (mods/\*/folder/filename.\*)

---

## StartClass

```cpp
QScriptClassCreator StartClass(const char* name, QScriptClass parent)
```

Returns a [[QScriptClassCreator]]

---

## AddMethod

```cpp
void AddMethod(QScriptClassCreator creator, const char* name, QType* params, QCFunc func, bool is_private = false)
```

Adds a method to the class creator. Takes a name, [[QType]] list which will be the parameters, [[QCFunc]] which will be the callback, and an optional [is_private][Private_Members] bool.

---

## AddScriptingMethod

```cpp
void AddScriptingMethod(QScriptClassCreator creator, const char* name, QScriptCallback callback, bool is_private)
```

Adds a scripting language method for the class creator. Takes a name, [[QScriptCallback]] which will be called when the method is called, and an optional is_private bool.

---

## AddVariable

```cpp
void AddVariable(QScriptClassCreator creator, const char* name, QType type, QValue defaultval, bool is_private)
```

Adds a variable with a default value to the class creator. Takes a name, QType, [[QValue]], and an optional is_private bool.

Do **not** use this for adding strings. Use the next method instead.

---

## AddString

```cpp
void AddString(QScriptClassCreator creator, const char* name, const char* defaultval, bool is_private)
```

Adds a string variable to the class creator. Takes a name, a default value and an optional is_private bool.

---

## FinishClass

```cpp
QScriptClass FinishClass(QScriptClassCreator creator)
```

Finishes the class creator and returns a [[QScriptClass]]. Will delete the creator.

---

## CreateObject

```cpp
QScriptObject CreateObject(QScriptClass cls)
```

Returns a new [[QScriptObject]]. Takes a class from which to create the object.

---

## InitializeObject

```cpp
void InitializeObject(QScriptObject object)
```

Initializes a QScriptObject. Call every time after you create one! Takes a QScriptObject.

---

## GetObjectValueIndex

```cpp
int GetObjectValueIndex(QScriptObject object, const char* name)
```

Gets a index of a variable from the object. Takes a QScriptObject and a name of the variable.

---

## SetObjectValue

```cpp
void SetObjectValue(QScriptObject object, int index, QValue val)
```

Sets a value inside an object. Takes the object, the index of the value, and a QValue. Do **not** use this function for setting strings.

---

## SetObjectString

```cpp
void SetObjectString(QScriptObject object, int index, const char* str)
```

Sets a string inside an object. Takes the object, the index of the value and a string.

---

## GetObjectValue

```cpp
QValue GetObjectValue(QScriptObject object, int index)
```

Gets a value from an object. Returns a QValue and takes the object and the index of the value.

---

## GetObjectValueType

```cpp
QType GetObjectValueType(QScriptObject object, int index)
```

Gets the type of a value in the object. Takes the object and the index of the value. Returns a QType.

---

## GetObjectMethodIndex

```cpp
int GetObjectMethodIndex(QScriptObject object, const char* name)
```

Gets the index of a method in the object. Takes the object and the name of the method.

---

## GetObjectMethod

```cpp
QScriptFunction GetObjectMethod(QScriptObject object, int index)
```

Gets the method of an object. Takes the object and the index of the method. Returns a [[QScriptFunction]].

---

## CallObjectMethod

```cpp
QReturn CallObjectMethod(QScriptObject object, int index, QScriptArgs arguments);
```

Calls a method from the object. Takes the object, index of the method and [[QScriptArgs]].

---

## GetArgValue

```cpp
QValue GetArgValue(QScriptArgs args, int index)
```

Gets a value from some arguments. Takes a QScriptArgs and the argument index.

---

## GetArgType

```cpp
QType GetArgType(QScriptArgs args, int index)
```

Gets the type of the argument from a QScriptArgs. Takes a QScriptArgs and the argument index.

---

## CallFunction

```cpp
void CallFunction(QScriptFunction function, const char* fmt, ...)
```

Calls a QScriptFunction, takes a string which represents the types of arguments and a vararg which are the arguments themselves. The arguments are normal C++ types.

Here is a table of chars to QType

{{CharToType}}

---