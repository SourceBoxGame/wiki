# QScript Rundown Page 4

By the nature of QScript, it has been designed to be a appframework interface. It means that anything in the game can use it.

If you want to use QScript in your own dll, first you have to connect to it.

Use the `CreateInterfaceFn` function with the `QSCRIPT_INTERFACE_VERSION` parameter which will return a (IQScript*).

$_SMALL Remember to check for null values! _$
```cpp
qscript = (IQScript*)appSystemFactory(QSCRIPT_INTERFACE_VERSION, NULL)
```

(appSystemFactory is a `CreateInterfaceFn` you get in the `Init` or `Connect` function of a DLL class)
