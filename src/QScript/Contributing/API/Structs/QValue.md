# QValue

    union QValue
    {
        int value_int;
        float value_float;
        const char* value_string;
        char* value_modifiable_string;
        bool value_bool;
        QScriptFunction value_function;
        QScriptObject value_object;
    };

QValue is used everywhere in QScript. It is used for storing all sorts of values.