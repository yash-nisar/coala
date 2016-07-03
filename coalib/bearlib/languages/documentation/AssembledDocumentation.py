from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)

Description = DocumentationComment.Description
Parameter = DocumentationComment.Parameter
ReturnValue = DocumentationComment.ReturnValue


def assemble_documentation(doccomment, docstyle_definition,
                           marker, indent, range):
    """
    Assembles a list of parsed documentation comments.

    This function just assembles the documentation comment
    itself, without the markers and indentation.

    :param doccomment:
        The list of parsed documentation comments.
    :param param_sym:
        A two element tuple that defines how a param definition starts and
        ends in a documentation comment.
    :param ret_sym:
        A string that defines how a return statement definition occurs in
        a documentation comment.
    """
    assembled_doc = ""
    for section in doccomment:
        section_desc = section.desc.splitlines(keepends=True)

        if isinstance(section, Description):
            assembled_doc += section_desc[0]

        elif isinstance(section, Parameter):
            assembled_doc += (docstyle_definition.metadata.param_start +
                              section.name +
                              docstyle_definition.metadata.param_end +
                              section_desc[0])

        else:
            assert isinstance(section, ReturnValue)
            assembled_doc += docstyle_definition.metadata.return_sep + \
                section_desc[0]

        for desc in section_desc[1:]:
            assembled_doc += desc

    return DocumentationComment(assembled_doc, docstyle_definition, indent,
                                marker, range)
