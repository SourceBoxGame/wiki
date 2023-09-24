# QScript API

---

## CreateModule

    QScriptModule CreateModule(const char* name, QModuleDefFunc* funcs)

Takes a name, and a [[QModuleDefFunc]] list, returns a QScriptModule

---

## LoadMods

    void LoadMods(const char* filename)

Will load a file inside the root of every mod.

---

## LoadModsInDirectory

    void LoadModsInDirectory(const char* folder, const char* filename)

Acts like LoadMods, but loads a file inside a subdirectory. (mods/\*/folder/filename.\*)

---

## StartClass

    QScriptClassCreator StartClass(const char* name, QScriptClass parent)

Returns a [[QScriptClassCreator]]

---

## AddMethod

    void AddMethod(QScriptClassCreator creator, const char* name, QType* params, QCFunc func, bool is_private = false)

Adds a method to the class creator. Takes a name, [[QType]] list which will be the parameters, [[QCFunc]] which will be the callback, and an optional [is_private][Private_Members] bool.

---

## AddScriptingMethod

    void AddScriptingMethod(QScriptClassCreator creator, const char* name, QScriptCallback callback, bool is_private)

Adds a scripting language method for the class creator. Takes a name, [[QScriptCallback]] which will be called when the method is called, and an optional is_private bool.

---

## AddVariable

    void AddVariable(QScriptClassCreator creator, const char* name, QType type, QValue defaultval, bool is_private)

Adds a variable with a default value to the class creator. Takes a name, QType, [[QValue]], and an optional is_private bool.

Do **not** use this for adding strings. Use the next method instead.

---

## AddString

    void AddString(QScriptClassCreator creator, const char* name, const char* defaultval, bool is_private)

Adds a string variable to the class creator. Takes a name, a default value and an optional is_private bool.

---

## FinishClass

    QScriptClass FinishClass(QScriptClassCreator creator)

Finishes the class creator and returns a [[QScriptClass]]. Will delete the creator.

---