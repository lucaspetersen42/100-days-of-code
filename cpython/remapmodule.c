#include <Python.h>

// Function
int Cremap(inp1, inp2, out1, out2, val_in)
{
    return (val_in - inp1) / (inp2 - inp1) * (out2 - out1) + out1;
}


// PyObject
static PyObject* remap(PyObject* self, PyObject* args)
{
    int inp1, inp2, out1, out2, val_in, val_out;

    if (!PyArg_ParseTuple(args, "ii", &inp1, &inp2, &out1, &out2))
        return NULL;
    val_out = cremap(inp1, inp2, out1, out2, val_in)
    return PyLong_FromLong(val_out);
}

static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "Version 0.01");
}

static PyMethodDef Examples[] = {
    {"remap", remap, METH_VARARGS, "Função map do Processing."},
    {"version", (PyCFunction)version, METH_NOARGS, "returns the version of the module"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Example = {
    PyModuleDef_HEAD_INIT,
    "Example",
    "remap Module",
    -1,  // global state
    Examples
};


// Initializer Function
PyMODINIT_FUNC PyInit_Example(void)
{
    return PyModule_Create(&Example)
}

// Method Definition


// Module Definition

