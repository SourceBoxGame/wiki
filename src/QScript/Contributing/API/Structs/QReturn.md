# QReturn

    struct QReturn
    {
        enum QType type;
        QValue value;
    };

QReturn is a struct which contains a [[QType]] and a [[QValue]]

The data in the QValue must match the QType.