# md2pptx
Markdown to Powerpoint Converter

**Note:** md2pptx only supports Python 3. So the installation instructions are for that.

**Usage:**

  `python3 md2pptx output.pptx < input.markdown`

or

  `md2pptx output.pptx < input.markdown`

### Installation

Installation is straightforward:

1. Install python-pptx
2. Clone md2pptx into a new directory

The md2pptx repo includes all the essentials, such as funnel.py. You don't install these with eg pip. There are some optional packages, outlined in the User Guide.

You can install python-pptx with

  `pip3 install python-pptx`

(On a Raspberry Pi you might want to use `pip3` (or `python3 -m pip`) to install for Python 3.)

You will probably need to issue the following command from the directory where you install it:

  `chmod +x md2pptx`

### Starting To Use md2pptx

I would also suggest you start with a presentation that references Martin Template.pptx in the metadata (before the first blank line). \
Here is a very simple deck that does exactly that.

```
template: Martin Template.pptx

# This Is A Presentation Title Page

## This Is A Presentation Section Page

### This Is A Bulleted List Page

* One
    * One A
    * One B
* Two

Here are some slide notes. Note you leave an empty line between the content - in this case a bulleted list - and the notes.

You can do multiple paragraphs and even use symbols.
```

