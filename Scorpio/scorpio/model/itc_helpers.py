#!/usr/bin/env python

"""
Module containing classes associated with ITC experiments and data.
"""

class ITCInstrument(object):
    """
    ITC instrument class.

    E.g. VP-ITC Microcalorimeter

    Attributes:
      * name - name of calorimeter

    Examples:
      >>> from itc_helpers import ITCInstrument
      >>> instrument = ITCInstrument('VP-ITC Microcalorimeter')
      >>> instrument
      <ITCInstrument('VP-ITC Microcalorimeter')>
      >>> instrument.name
      'VP-ITC Microcalorimeter'

    """
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return "<ITCInstrument('%s')>" % self._name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def _get_name(self):
        return self._name
    def _set_name(self, name):
        self._name = name
    name = property(_get_name, _set_name)

class ITCInteractionType(object):
    """
    ITC interaction type class.

    E.g. Biological

    Attributes:
      * interaction_type - interaction type

    Examples:
      >>> from itc_helpers import ITCInteractionType
      >>> interaction_type = ITCInteractionType('Biological')
      >>> interaction_type
      <ITCInteractionType('Biological')>
      >>> interaction_type.interaction_type
      'Biological'

    """
    def __init__(self, interaction_type):
        self._interaction_type = interaction_type

    def __repr__(self):
        return "<ITCInteractionType('%s')>" % self._interaction_type

    def __eq__(self, other):
        return self.interaction_type == other.interaction_type

    def __ne__(self, other):
        return self.interaction_type != other.interaction_type

    def _get_interaction_type(self):
        """
        Return interaction_type.
        """
        return self._interaction_type

    def _set_interaction_type(self, interaction_type):
        """
        Set interaction_type name.
        """
        self._interaction_type = interaction_type

    interaction_type = property(_get_interaction_type, _set_interaction_type)

class ITCBuffer(object):
    """
    ITC itc_buffer class.

    E.g.
    NaCl 100 mM
    HEPES 100 mM

    Attributes:
      * itc_buffer - itc_buffer used in itc experiment

    Examples:
      >>> from itc_helpers import ITCBuffer
      >>> itc_buffer_text = 'NaCl 100 nM, HEPES 100 nM'
      >>> b = ITCBuffer(itc_buffer_text)
      >>> print b.description
      NaCl 100 nM, HEPES 100 nM

    """
    def __init__(self, description):
        self._description = description

    def _get_description(self):
        """
        Return description.
        """
        return self._description

    def _set_description(self, description):
        """
        Set description.
        """
        self._description = description

    description = property(_get_description, _set_description)

class ITCComment(object):
    """
    ITC comment class.

    Attributes:
      * comment - comment on itc experiment

    Examples:
      >>> from itc_helpers import ITCComment
      >>> comment = ITCComment('Rounding error')
      >>> comment
      <ITCComment('Rounding error')>
      >>> comment.comment
      'Rounding error'

    """
    def __init__(self, comment, comment_definition=None):
        self._comment = comment
        self._definition = comment_definition

    def __repr__(self):
        return "<ITCComment('%s')>" % self._comment

    def _get_comment(self):
        """
        Return comment.
        """
        return self._comment

    def _set_comment(self, comment):
        """
        Set comment.
        """
        self._comment = comment

    comment = property(_get_comment, _set_comment)

    def _get_definition(self):
        if self._definition:
            return self._definition.definition
        else:
            return None
    def _set_definition(self, definition):
        assert isinstance(definition, ITCCommentDefinition)
        self._definition = definition
        
    definition = property(_get_definition, _set_definition)

    @property
    def definition_id(self):
        """
        Return comment definition id.
        """
        if self._definition:
            return self._definition.id
        else:
            return None
        
class ITCCommentDefinition(object):
    """
    ITC comment definition class.

    Attributes:
      * definition - categorisation of itc comment

    Examples:
      >>> from itc_helpers import ITCCommentDefinition
      >>> definition = ITCCommentDefinition('Error')
      >>> definition
      <ITCCommentDefinition('Error')>
      >>> definition.definition
      'Error'

    """
    def __init__(self, definition):
        self._definition = definition

    def __repr__(self):
        return "<ITCCommentDefinition('%s')>" % self._definition

    def _get_definition(self):
        """
        Return definition.
        """
        return self._definition

    def _set_definition(self, definition):
        """
        Set definition.
        """
        self._definition = definition

    definition = property(_get_definition, _set_definition)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)

