from pymongo.son_manipulator import SONManipulator


class AutoincrementId(SONManipulator):
    """A son manipulator that adds the autoincrement ``_id`` field.

    Adding only occurs if ``_id`` missing in son object.

    Usage example::

        db.add_son_manipulator(AutoincrementId())
    """

    def transform_incoming(self, son, collection):
        """Add an ``_id`` field if it's missing.

        :param son: a son object (document object)
        :param collection: a collection for inserting
        """
        if "_id" not in son:
            son["_id"] = self._get_next_id(collection)
        return son

    def _get_next_id(self, collection):
        """Retrieve an id for inserting into a certain collection.

        :param collection: a collection for inserting
        """
        database = collection.database
        result = database._autoincrement_ids.find_and_modify(
                     query={"_id": collection.name,},
                     update={"$inc": {"next": 1},},
                     upsert=True,  # insert if object doesn’t exist
                     new=True,     # return updated rather than original object
                 )
        return result["next"]