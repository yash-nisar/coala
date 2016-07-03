import unittest

from coalib.bearlib.languages.documentation.AssembledDocumentation import (
    assemble_documentation)
from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation)
from tests.bearlib.languages.documentation.TestUtils import (
    load_testdata)


class AssembledDocumentationTest(unittest.TestCase):

    def test_python_assembly(self):

        data = load_testdata("default.py")

        original = [doc.documentation for doc in
                    extract_documentation(data, "python", "default")]

        parsed_docs = [(doc.parse(), doc.marker, doc.indent, doc.range)
                       for doc in
                       extract_documentation(data, "python", "default")]

        docstyle_definition = DocstyleDefinition.load("python", "default")

        assembled_docs = [assemble_documentation(doc[0], docstyle_definition,
                                                 doc[1], doc[2], doc[3])
                          for doc in parsed_docs]

        self.assertEqual([str(doc) for doc in assembled_docs], original)

        for assembled_doc in assembled_docs:
            self.assertIn(assembled_doc.assemble(), "".join(data))
