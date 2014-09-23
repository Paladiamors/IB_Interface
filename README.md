IB_Interface
============


Objective
=========

The objective of this library is to create a more maintainable Python interface library to the interactive brokers API.

Experience in the past in attempting to resurrect the IbPy for use with latest version of the api has been a painful process, requiring learning of the swig library and retooling of the C code to allow Python to interface with the library. The biggest pain with interacting with the C library is the lack of a simple way of allowing the event loop interact with the created python callback in a simple manner without needing to perform some level of modification of the C code and creation of an event loop to do call back interaction in Python. After abandonding attempts to interface with C API, I've thus moved onto using the java API where Jython is able to directly create java code that can be called by the event callback handlers. This strategy eliminates the need to maintain a Python event loop to interact with the data from IB, which was main maintainability problem with the IbPy library.