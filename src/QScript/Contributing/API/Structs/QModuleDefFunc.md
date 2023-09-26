# QModuleDefFunc

```cpp
struct QModuleDefFunc
{
    QCFunc func;
    const char* name;
    enum QType ret;
    const char* types;
};
```

QModuleDefFunc is used for defining functions that QScript will bind to the scripting languages.

`types` is a string of characters that represent the types of parameters which the function accepts. QScript will automatically check the types for you, so do not worry about checking them yourself.

Here is a list of all the types and their characters:

{{CharToType}}

`ret` is what the function will return.

`func` is a [[QCFunc]] which will be called when a scripting langauge calls your function.

Here is an example list of QModuleDefFuncs which you pass to [CreateModule][QScript/Contributing/API/qscript]

```cpp
static QModuleDefFunc sourcebox_client[] = {
    {QScriptClientMsg,"Msg",QType_None,"s"},
    {RegisterCmd,"RegisterCmd",QType_None,"sp"},
    {0,0,QType_None,0}
    //{RegisterCmd,"RegisterCmd",QType_None,"sp"},
};
```