# QScript Rundown Page 3

Lets talk about `QObject`s.

A full `QObject` structure looks like this:

```cpp
struct QObject
{
    struct QClass* cls;
    union QValue vars[];
};
```

The structure is pretty complex.

Lets try to understand it piece by piece.

A `QObject` contains a pointer to a `QClass`. The `QClass` pointer is shared by `QObject`s which use the same class.
The QObject also contains a list of [QValues][QValue] which are the individual unique variables of the QObject.

---

```cpp
struct QClass
{
    const char* name;

    int vars_count;
    struct QVar* vars;

    int methods_count;
    struct QFunction* methods;

    int sigs_count;
    struct QInterface** sigs;
};
```

Let's go one level deeper and this is where we start to branch out. We will tackle `QVar* vars` first.

---

```cpp
struct QVar
{
    enum QType type;
    const char* name;
    int size;
    bool is_private;
    union QValue defaultval;
};
```

`QVar` is basically a definition of a variable in a class. It stores the name, type, default value, etc. The `size` is used to determine the initial size of the string if the `type` is a `QType_String`

A `QClass` will store a pointer to a list of these, along with the amount. They are in fact, used as a reference to the `QValue vars[]` which are a 1:1 representation of the `QVar* vars*` in the class. In other words, an index in the `QVar* vars*` array in the `QClass` corresponds to the value in `QValue vars[]` in the QObject.

---

```cpp
enum QFunctionType
{
    QFunction_Native,
    QFunction_Scripting,
    QFunction_Module,
    QFunction_Void,
};

struct QFunction
{
    int always_zero;
    enum QFunctionType type;
    union 
    {
        QCFunc func_native;
        QCallback* func_scripting;
        QModuleFunction* func_module;
        void* func_void;
    };
};
```

`QFunction` is more of a wrapper around multiple types of functions. The each slot in the union has a corresponding `QFunctionType`. But what you might notice is the `always_zero` variable. Why is it there?

There is this quirk with scripting languages where they will write their entire scripting base libraries in their own C api, and then pass these base library functions as a normal pointer to the language. Which basically means that they will treat every C function as a regular function pointer and not a struct. Function pointers have a very special tendency to not be 0 (DUH). 
We can take advantage of that by first checking if the `QFunction` `always_zero` is 0, and if its not, we just CALL the QFunction pointer directly. But if it is 0, we can be 99.9% sure that it is actually a `QFunction` struct and we can treat it as such.

---

```cpp
typedef struct
{
    int count;
    enum QType* types;
} QParams;

typedef struct 
{
    int count;
    const char** names;
    struct QParams* args;
} QInterface;
```

A `QInterface` is a list of function declarations. Not definitions. A `QInterface` only stores the name, and arguments of each function. The actual implementation is up to the `QClass`.

When a `QClass` inherits from another `QClass`, it creates a new `QInterface` the parent `QInterface` **pointers** get copied into the interface array before the new one. Not the `QInterface`s themselves. This saves on memory.

We plan on adding actual interface functionality to the scripting languages, showing off to functional scripting language developers what modern OOP languages can do.

---

[<- Prev][QScriptRundown2.md] | [Next ->][QScriptRundown4.md]
