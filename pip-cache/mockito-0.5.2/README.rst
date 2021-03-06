Mockito is a spying framework based on Java library with the same name.

1. To install:

  $ python setup.py install

2. To run all tests:

  $ python setup.py test

3. For more info, see:

  __ http://code.google.com/p/mockito-python/
  
  Feel free to contribute more documentation or feedback!

4. Our user and developer discussion group is:

  __ http://groups.google.com/group/mockito-python

5. Mockito is licensed under the MIT license

6. Library was tested with the following Python versions:

  Python 2.4.6
  Python 2.5.4
  Python 2.6.1
  Python 2.7
  Python 3.1.2
  
7. (Generated from mockito_demo_test.py) Basic usage:

  import unittest
  from mockito import mock, when, verify
  
  class DemoTest(unittest.TestCase):
    def testStubbing(self):
      # create a mock
      ourMock = mock()
  
      # stub it
      when(ourMock).getStuff("cool").thenReturn("cool stuff")
      
      # use the mock
      self.assertEqual("cool stuff", ourMock.getStuff("cool"))
      
      # what happens when you pass different argument?
      self.assertEqual(None, ourMock.getStuff("different argument"))
      
    def testVerification(self):
      # create a mock
      theMock = mock()
  
      # use the mock
      theMock.doStuff("cool")
      
      # verify the interactions. Method and parameters must match. Otherwise verification error.
      verify(theMock).doStuff("cool")
    
  