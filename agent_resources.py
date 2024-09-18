import random

from consts import Consts

class Resources: 
    """
    Represents a group of resources that agents can generate, metabolize, and share.

    Attributes:
        types (list): List of available resource types.
        amount (dict): Dictionary holding the amount of each resource type.

    Methods:
        generate(self, resource_type, amount)
        metabolize(self, resource_type, amount)
        get_resource_levels(self)
    """

    TYPES = ["sugar", "spice", "grain", "water", "oil"]
    _MAX_RESOURCE = Consts.MAX_AMOUNT_OF_ANY_RESOURCE

    def __init__(self):
        self.amount = {resource_type: random.uniform(5.0, self._MAX_RESOURCE) for resource_type in self.TYPES}

    def generate(self, resource_type, amount):
        """
        Generate a specified amount of a resource type.

        Args:
            resource_type (str): The type of resource to generate.
            amount (float): The amount of resource to generate.
        """
        if resource_type in self.TYPES:
            self.amount[resource_type] += amount
            self.amount[resource_type] = min(self._MAX_RESOURCE, self.amount[resource_type])

    def metabolize(self, resource_type, amount):
        """
        Metabolize (reduce) a specified amount of a resource type.

        Args:
            resource_type (str): The type of resource to metabolize.
            amount (float): The amount of resource to metabolize.

        Returns:
            bool: True if there was enough resource to metabolize, False otherwise.
        """
        if resource_type in self.TYPES:
            self.amount[resource_type] -= amount
            self.amount[resource_type] = max(0.0, self.amount[resource_type])
            return True
        return False

    def get_resource_levels(self):
        """
        Get the current amount of each resource type.

        Returns:
            dict: A dictionary of resource types and their amounts.
        """
        return self.amount
    
    def get_amount(self, resource_type):
        """
        Get the current amount of a specific resource type.

        Args:
            resource_type (str): The type of resource to check.

        Returns:
            float: The amount of the specified resource.
        """
        return self.amount.get(resource_type, 0.0)