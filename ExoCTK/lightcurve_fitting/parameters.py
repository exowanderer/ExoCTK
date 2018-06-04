"""Base and child classes to handle orbital parameters

Author: Joe Filippazzo
Email: jfilippazzo@stsci.edu
"""
import os

class Parameter:
    """A generic parameter class"""
    def __init__(self, name, value, vary=True, mn=None, mx=None):
        """Instantiate a Parameter with a name and value at least
        
        Parameters
        ----------
        name: str
            The name of the parameter
        value: float, int, str, list, tuple
            The value of the parameter
        vary: bool
            Is this a free parameter?
        mn: float, int, str, list, tuple (optioal)
            The minimum value
        mx: float, int, str, list, tuple (optioal)
            The maximim value
        """
        self.name = name
        self.value = value
        self.mn = mn
        self.mx = mx
        self.vary = vary
        
    @property
    def values(self):
        """Return all values for this parameter"""
        vals = self.name, self.value, self.vary, self.mn, self.mx
        
        return tuple(filter(lambda x: x is not None, vals))
        

class Parameters:
    """A class to hold the Parameter instances
    """
    def __init__(self, param_file=None, **kwargs):
        """Initialize the parameter object
        
        Parameters
        ----------
        param_file: str
            A text file of the parameters to parse
        
        Example
        -------
        params = lightcurve.Parameters(a=20, ecc=0.1, inc=89, limb_dark='quadratic')
        """
        self.__dict__['list'] = []
        
        # Make an empty params dict
        params = {}

        # If a param_file is given, make sure it exists
        if param_file is not None and os.path.exists(param_file):

            # Parse the ASCII file
            if param_file.endswith('.txt'):

                # Add the params to a dict
                data = np.genfromtxt(param_file)
                params = {i:j for i,j in data}

            # Parse the JSON file
            elif param_file.endswith('.json'):

                with open(param_file) as json_data:
                    params = json.load(json_data)

        # Add any kwargs to the parameter dict
        params.update(kwargs)

        # Try to store each as an attribute
        for param, value in params.items():
            setattr(self, param, value)
            
            
    def __setattr__(self, item, value):
        """Maps attributes to values
        """
        # Convert single items to tuple
        if isinstance(value, (str, float, int, bool)):
            value = (value,)

        # Convert list to tuple
        if isinstance(value, list):
            value = tuple(value)

        if not isinstance(value, tuple):
            raise TypeError("Cannot set {}={}.".format(item, value))

        # Set the attribute
        self.__dict__[item] = Parameter(item, *value)
        
        # Add it to the list of parameters
        self.__dict__['list'].append(self.__dict__[item].values)