# IBaseScriptingInterface

This interface is what you inherit from if you want to make a new language interface.

Here is how it looks like in the code:

$_SMALL public/qscript/qscript_language.h _$
```cpp
abstract_class IBaseScriptingInterface : public CBaseAppSystem<IAppSystem>
{
public:
    virtual InitReturnVal_t Init() = 0;
    virtual void Initialize() = 0;
    virtual bool Connect(CreateInterfaceFn factory) = 0;
    virtual void Shutdown() = 0;
    virtual void ImportModules(CUtlVector<QModule*>* modules) = 0;
    virtual QInstance* LoadMod(QMod* mod, const char* path) = 0;
    virtual QReturn CallCallback(QCallback* callback, QArgs* args) = 0;
};
```

Here is a rundown of all the functions.

---

## Init

Gets called after `Connect()`. I suggest that you dont do anything here and just return `INIT_OK`.

---

## Initialize

Unused.

---

## Connect

Gets called before anything else. This is where you connect everything you need.

---

## Shutdown

Gets called upon shutdown.

---

## ImportModules

Gets called when QScript has finished importing all modules. (During PostInit)

---

## LoadMod

Loads a single file and gets the mod its from. Must return a QInstance or 0 if the path's file extension doesnt match the language.

---

## CallCallback

Calls the QCallback with the specified QArgs. You mustnt check if the QCallback is correct, it should already be.

---

Much more is going on under the hood. Read [page 5 of the QScript Rundown][QScriptRundown5]