
import unittest

from markdown_functions import markdown_to_blocks
from blocktype import block_to_block_type
from blocktype import BlockType
from markdown_blocks import markdown_to_html_node
from markdown_blocks import markdown_to_blocks


class TestMarkDownFunctions(unittest.TestCase):
    def test_markdown_functions(self):
        answer = ["This",   
                  "will",              
                  "hurt",
                  "you."]
        test_data = "This \n\n will\n\n hurt \n\n you."
        test = markdown_to_blocks(test_data)

        self.assertEqual(answer, test)

    def test_markdown_functions2(self):
        answer = ["This",   
                  "will",              
                  "hurt",
                  "you."]
        test_data = "This       \n\n will\n\n  hurt\n\n you."
        test = markdown_to_blocks(test_data)

        self.assertEqual(answer, test)

    def test_markdown_functions3(self):
        answer = ["This is a paragraph. \nThis is a new paragraph.",   
                  "Will you ever understand?",              
                  "Hurt the ones that made you cry.",
                  "You are the   best."]
        test_data = "This is a paragraph. \nThis is a new paragraph.\n\n Will you ever understand?\n\n Hurt the ones that made you cry. \n\n You are the   best."
        test = markdown_to_blocks(test_data)

        self.assertEqual(answer, test)

    def test_block_to_block_type_not_heading(self):
        # 7 #'s should NOT be a heading
        block = "####### too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
      