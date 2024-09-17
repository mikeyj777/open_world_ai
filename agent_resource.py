import random

class Resource:
    """
    Represents a resource that agents can generate, metabolize, and share.

    Attributes:
        types (list): List of available resource types.
        amount (dict): Dictionary holding the amount of each resource type.
    """

    TYPES = ["sugar", "spice", "grain", "water", "oil"]

    def __init__(self):
        self.amount = {resource_type: random.uniform(5.0, 15.0) for resource_type in self.TYPES}

    def generate(self, resource_type, amount):
        """
        Generate a specified amount of a resource type.

        Args:
            resource_type (str): The type of resource to generate.
            amount (float): The amount of resource to generate.
        """
        if resource_type in self.TYPES:
            self.amount[resource_type] += amount

    def metabolize(self, resource_type, amount):
        """
        Metabolize (reduce) a specified amount of a resource type.

        Args:
            resource_type (str): The type of resource to metabolize.
            amount (float): The amount of resource to metabolize.

        Returns:
            bool: True if there was enough resource to metabolize, False otherwise.
        """
        if resource_type in self.TYPES and self.amount[resource_type] >= amount:
            self.amount[resource_type] -= amount
            return True
        return False

    def get_amount(self, resource_type):
        """
        Get the current amount of a specific resource type.

        Args:
            resource_type (str): The type of resource to check.

        Returns:
            float: The amount of the specified resource.
        """
        return self.amount.get(resource_type, 0.0)