# Term Project B

# Ellis Bissonnette (101200757)
# Anastacia Gorbenko (101181166)
# Zainab El Sharrif (101181197)

# March 10th, 2024

# IMD 3002A
# Ishtiaque Hossain

# -------------------------------------------------------------------------------------

import maya.cmds as cmds
import random as rnd

# Global constants
WINDOW_NAME = 'Term Project B'

DEFAULT_BLOCK_HEIGHT = 0.32
DEFAULT_BLOCK_WIDTH = 0.8
DEFAULT_BLOCK_DEPTH = 0.8

SIDED_BUMP_BLOCK_HEIGHT = 0.8

BUMP_RADIUS = 0.25
BUMP_HEIGHT = 0.2

# Objects
class BlockInfo:

    def __init__(self):

        self.namespace = ''
        self.colour = []

        self.width = 0
        self.height = 0
        self.depth = 0

        self.sizeX = 0
        self.sizeY = 0
        self.sizeZ = 0

# Functions ---------------------------------------------------------------------------

# Setting up to create a block by getting user specified values, calculating dimensions, and creating a namespace
def setUpBlockCreation(customWidth = True, customHeight = True, customDepth = True, widthVar = '', heightVar = '', depthVar = '', colourVar = '', setWidth = 0, setHeight = 0, setDepth = 0):

    # Creating block object to store its information
    block = BlockInfo()

    # If there are slider values, get them
    # Otherwise set the set them to the set values
    if customWidth:
        block.width = cmds.intSliderGrp(widthVar, q = True, v = True)
    else:
        block.width = setWidth

    if customHeight:
        block.height = cmds.intSliderGrp(heightVar, q = True, v = True)
    else:
        block.height = setHeight

    if customDepth:
        block.depth = cmds.intSliderGrp(depthVar, q = True, v = True)
    else:
        block.depth = setDepth

    block.colour = cmds.colorSliderGrp(colourVar, q = True, rgbValue = True)

    # Scaling dimensions to appropriate values
    block.sizeX = block.width * DEFAULT_BLOCK_WIDTH
    block.sizeY = block.height * DEFAULT_BLOCK_HEIGHT
    block.sizeZ = block.depth * DEFAULT_BLOCK_DEPTH

    # Generating a random namespace for the block
    block.namespace = createNamespace()

    return block

# -------------------------------------------------------------------------------------

# Creating and setting new namespace
def createNamespace():

    # Generating a random namespace
    namespace = 'Block' + str(rnd.randint(1000, 9999))

    # Clearing anything selected
    cmds.select(clear = True)

    # Creating a new namespace and moving into it
    cmds.namespace(add = namespace)
    cmds.namespace(set = namespace)

    return namespace

# -------------------------------------------------------------------------------------

# Calculating bump spacing
def bumpSpacing(bumpNum, sectionSize, dimension):
    return ((bumpNum * sectionSize) - (dimension / 2.0) + (sectionSize / 2.0))

# -------------------------------------------------------------------------------------

# Creating a top bump on selected block
def topBump(block, i, j, baseWidth, baseDepth):

    cmds.polyCylinder(r = BUMP_RADIUS, h = BUMP_HEIGHT)

    cmds.move((block.sizeY + (BUMP_HEIGHT / 2)), moveY = True, a = True)
    cmds.move(bumpSpacing(i, baseWidth, block.sizeX), moveX = True, a = True)
    cmds.move(bumpSpacing(j, baseDepth, block.sizeZ), moveZ = True, a = True)

# -------------------------------------------------------------------------------------
    
# Creating a side bump on selected block
def zBump(block, i, j, direction):

    cmds.polyCylinder(r = BUMP_RADIUS, h = BUMP_HEIGHT)

    cmds.rotate(90, rotateX = True, a = True)

    cmds.move((direction * ((block.sizeZ / 2) + (BUMP_HEIGHT / 2))), moveZ = True, a = True)
    cmds.move((block.sizeY - (i * SIDED_BUMP_BLOCK_HEIGHT) - (SIDED_BUMP_BLOCK_HEIGHT / 2)), moveY = True, a = True)
    cmds.move(bumpSpacing(j, DEFAULT_BLOCK_WIDTH, block.sizeX), moveX = True, a = True)

# -------------------------------------------------------------------------------------
    
# Creating a side bump on selected block
def xBump(block, i, j, direction):

    cmds.polyCylinder(r = BUMP_RADIUS, h = BUMP_HEIGHT)

    cmds.rotate(90, rotateX = True, a = True)
    cmds.rotate(90, rotateY = True, a = True)

    cmds.move((direction * ((block.sizeX / 2) + (BUMP_HEIGHT / 2))), moveX = True, a = True)
    cmds.move((block.sizeY - (i * SIDED_BUMP_BLOCK_HEIGHT) - (SIDED_BUMP_BLOCK_HEIGHT / 2)), moveY = True, a = True)
    cmds.move(bumpSpacing(j, DEFAULT_BLOCK_DEPTH, block.sizeZ), moveZ = True, a = True)

# -------------------------------------------------------------------------------------

# Creating base of standard block
def blockBase(block):

    # Creating block base and moving it to sit on the grid
    cmds.polyCube(h = block.sizeY, w = block.sizeX, d = block.sizeZ, sx = block.width, sy = (block.height - 1), sz = block.depth)
    cmds.move((block.sizeY / 2.0), moveY = True, a = True)

    # Creating block bumps
    for i in range(block.width):

        for j in range(block.depth):
            topBump(block, i, j, DEFAULT_BLOCK_WIDTH, DEFAULT_BLOCK_DEPTH)

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

# -------------------------------------------------------------------------------------

# Creating a standard block based on user inputed slider values
def standardBlock():

    block = setUpBlockCreation(customWidth = True, customHeight = True, customDepth = True, widthVar = 'standardWidth', heightVar = 'standardHeight', depthVar = 'standardDepth', colourVar = 'standardColour')

    # Creating block
    blockBase(block)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------
    
# Creating a tile block based on user inputed slider values
def tileBlock():

    block = setUpBlockCreation(customWidth = True, customHeight = False, customDepth = True, widthVar = 'tileWidth', depthVar = 'tileDepth', colourVar = 'tileColour', setHeight = 1)

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Creating block and moving it to sit on the grid
    cmds.polyCube(h = block.sizeY, w = block.sizeX, d = block.sizeZ, sx = block.width, sy = (block.height - 1), sz = block.depth)
    cmds.move((block.sizeY / 2.0), moveY = True, a = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------
    
# Creating a jumper block based on user inputed slider values
def jumperBlock():

    # Setting up to create block
    block = setUpBlockCreation(customWidth = True, customHeight = True, customDepth = True, widthVar = 'jumperWidth', heightVar = 'jumperHeight', depthVar = 'jumperDepth', colourVar = 'jumperColour')

    # Adjusting width and depth to account for jumper block
    block.sizeX *= 2
    block.sizeZ *= 2

    # Creating block base and moving it to sit on the grid
    cmds.polyCube(h = block.sizeY, w = block.sizeX, d = block.sizeZ, sx = block.width, sy = (block.height - 1), sz = block.depth)
    cmds.move((block.sizeY / 2.0), moveY = True, a = True)

    # Creating block bumps
    for i in range(block.width):

        for j in range(block.depth):
            topBump(block, i, j, DEFAULT_BLOCK_WIDTH * 2, DEFAULT_BLOCK_DEPTH * 2)

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------

# Creating a 4 sided block based on user inputed slider values
def fourSideBlock():

    # Setting up to create block
    block = setUpBlockCreation(customWidth = True, customHeight = True, customDepth = True, widthVar = 'fourSideWidth', heightVar = 'fourSideHeight', depthVar = 'fourSideDepth', colourVar = 'fourSideColour')

    # Adjusting height
    block.sizeY = (block.height * SIDED_BUMP_BLOCK_HEIGHT) + (SIDED_BUMP_BLOCK_HEIGHT / 4)

    # Creating base block
    blockBase(block)

    # Creating side bumps
    for i in range(block.height):

        # X axis
        for j in range(block.depth):
            xBump(block, i, j, 1)
            xBump(block, i, j, -1)

        # Z axis
        for j in range(block.width):
            zBump(block, i, j, 1)
            zBump(block, i, j, -1)

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------

# Creating a round block based on user inputed slider values
def roundBlock():

    # Setting up to create block
    block = setUpBlockCreation(customWidth = False, customHeight = False, customDepth = False, colourVar = 'roundColour', setWidth = 1, setHeight = 1, setDepth = 1)

    # Splitting up the height 
    skinnySizeY = block.sizeY * 0.70
    wideSizeY = block.sizeY * 0.30
    
    # Creating the skinny part of the block base and moving it to sit on the grid
    cmds.polyCylinder(r = (block.sizeX / 2.5), h = skinnySizeY)
    cmds.move((skinnySizeY / 2), moveY = True, a = True)

    # Creating the wide part of the block base and moving it to sit on the skinny part
    cmds.polyCylinder(r = (block.sizeX / 2), h = wideSizeY)
    cmds.move((skinnySizeY + (wideSizeY / 2)), moveY = True, a = True)

    # Creating bump
    topBump(block, 0, 0, DEFAULT_BLOCK_WIDTH, DEFAULT_BLOCK_DEPTH)

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------
    
# Creating a thin jumper block based on user inputed slider values
def thinJumperBlock():

    # Setting up to create block
    thinJumperHeight = 1
    block = setUpBlockCreation(customWidth = True, customHeight = True, customDepth = False, widthVar = 'thinJumperWidth', heightVar = 'thinJumperHeight', colourVar = 'thinJumperColour', setDepth = 1)

    # Adjusting width and depth to account for thin jumper block
    block.sizeX *= 2
    block.sizeZ *= 1

    # Creating block base and moving it to sit on the grid
    cmds.polyCube(h = block.sizeY, w = block.sizeX, d = block.sizeZ, sx = block.width, sy = (block.height - 1), sz = block.depth)
    cmds.move((block.sizeY / 2.0), moveY = True, a = True)

    # Creating block bumps
    for i in range(block.width):

        for j in range(block.depth):
            topBump(block, i, j, DEFAULT_BLOCK_WIDTH * 2, DEFAULT_BLOCK_DEPTH)

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------

# Creating a standard block based on user inputed slider values
def cornerBlock():

    block = setUpBlockCreation(customWidth = False, customHeight = True, customDepth = False, heightVar = 'cornerHeight', colourVar = 'cornerColour', setWidth = 2, setDepth = 1)

    cmds.polyCube(h = block.sizeY, w = DEFAULT_BLOCK_WIDTH, d = block.sizeX, sx = 1, sy = 1, sz = 1)
    cmds.move((block.sizeX/2 - (DEFAULT_BLOCK_WIDTH/2)), moveX = True, a = True)
    cmds.move((block.sizeX/2 - (DEFAULT_BLOCK_WIDTH/2)), moveZ = True, a = True)
    cmds.move((block.sizeY/2), moveY = True, a = True)

    #create bumps
    for i in range(block.width):
        print("hi")
        cmds.polyCylinder(r = BUMP_RADIUS, h = BUMP_HEIGHT)

        cmds.move((block.sizeY + (BUMP_HEIGHT / 2)), moveY = True, a = True)
        cmds.move((block.sizeX/2 - (DEFAULT_BLOCK_WIDTH/2)), moveX = True, a = True)
        cmds.move(bumpSpacing(i, DEFAULT_BLOCK_WIDTH, block.sizeX) + (DEFAULT_BLOCK_WIDTH/2), moveZ = True, a = True)
        
    
    # Creating block
    blockBase(block)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------

# Creating a shelf block based on user inputed slider values
def shelfBlock():
    
    block = setUpBlockCreation(customWidth=False, customHeight=False, customDepth=False, colourVar='shelfColour', setWidth=4, setHeight=2, setDepth=1)

    # Create the vertical part of the shelf (back piece)
    vertical_height = block.sizeY * 3  # Thrice the block height for the back
    vertical = cmds.polyCube(h=vertical_height, w=block.sizeX * 0.6, d=block.sizeZ)
    cmds.move(vertical_height / 2, y=True)
    cmds.scale(1, 1, 0.6, vertical)
    

    # Create the horizontal part of the shelf (seat piece)
    horizontal_depth = block.sizeZ * 1.5  
    horizontal = cmds.polyCube(h=block.sizeY, w=block.sizeX * 0.6, d=horizontal_depth)
    cmds.move(block.sizeY + 0.3, y=True)  # Move up by its own height to be placed on top of the grid
    cmds.move(block.sizeZ, z=True)  # Move forward to not intersect with the back piece
    cmds.scale(1, 0.6, 1, horizontal)

    # Create two bumps on the horizontal part of the shelf
    for i in range(2):
        bump = cmds.polyCylinder(r=BUMP_RADIUS, h=BUMP_HEIGHT)
        cmds.rotate(180, x=True)
        # Calculate the X position for the bumps, they should be equidistant from the center of the shelf
        bump_x_pos = (-block.sizeX * 0.6 / 4) + (block.sizeX * 0.6 / 2 * i)
        cmds.move(bump_x_pos, x=True)
        # Position the bump so that its bottom sits on the top surface of the horizontal shelf
        cmds.move(block.sizeY + 0.59, y=True)
        #cmds.move(block.sizeY, y=True)   
        cmds.move(block.sizeZ + (horizontal_depth / 2) - (block.sizeZ / 2), z=True)

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# -------------------------------------------------------------------------------------
def sixBumpBlock():
    # Retrieve slider values for custom dimensions
    block = setUpBlockCreation(customWidth=False, customHeight=False, customDepth=False, colourVar='sixBumpColour', setWidth=2, setHeight=3, setDepth=1)

    # Create the vertical part of the block
    vertical = cmds.polyCube(w=block.sizeX, d=block.sizeZ, h=block.sizeY * 2)
    cmds.move(block.sizeY, y=True)  # Positioning at the origin on the grid
    cmds.rotate(0, '90deg', 0, vertical)  # Rotating 90 degrees on Y-axis

    # Add the top bumps
    for i in range(2):
        topBump(block, 0, i, DEFAULT_BLOCK_WIDTH, DEFAULT_BLOCK_DEPTH)
        cmds.move(0.4, x=True, relative=True)
        cmds.move(0.95, y=True, relative=True)
        cmds.move(-0.41, z=True, relative=True)

    # Create the front bumps
    for i in range(2):
        for j in range(2):
            xBump(block, j, i, 1)  # Adding 4 bumps on the front
            cmds.move(-0.4, x=True, relative=True)
            cmds.move(0.8, y=True, relative=True)
            cmds.move(-0.41, z=True, relative=True)

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)
    
# -------------------------------------------------------------------------------------
def fourBumpBlock():
    block = setUpBlockCreation(customWidth=False, customHeight=False, customDepth=False, colourVar='fourBumpColour', setWidth=2, setHeight=1, setDepth=1.5)

    # Create the main cube for the block
    mainBlock = cmds.polyCube(w=block.sizeX / 1.5, h=block.sizeY * 2, d=block.sizeZ * 1.5)
                             
    cmds.move(block.sizeY * 2, y=True)  # Move up to sit on the grid
    cmds.rotate(0, 0, '90deg', mainBlock)  # Rotating 90 degrees on X & Z-axis

    # Create and position the top bumps correctly
    for i in range(2):
        topBump(block, 0, i,  DEFAULT_BLOCK_WIDTH, DEFAULT_BLOCK_DEPTH)
        newYPosition = (block.sizeY * 3.6) + (BUMP_HEIGHT / 2)
        cmds.move(newYPosition, y=True, absolute=True)
        cmds.move(-0.2, z=True, relative=True)
        cmds.move(0.4, x=True, relative=True)
        

    # Create and position the front bumps correctly
    for i in range(2):
        xBump(block, 0, i, 1)
        cmds.move(block.sizeZ / 2 + BUMP_HEIGHT / 2, z=True, relative=True, objectSpace=True)
        # Adjust for correct placement in front
        cmds.move(-0.48, x=True, relative=True)
        cmds.move(1.45, y=True, relative=True)
        cmds.move(-0.2, z=True, relative=True)
        

    # Creating block material
    cmds.shadingNode('lambert', asShader = True, name = 'blockMat')
    cmds.setAttr(block.namespace + ':blockMat.color', block.colour[0], block.colour[1], block.colour[2], typ = 'double3')

    # Combining all block parts into one
    cmds.polyUnite((block.namespace + ':*'), n = block.namespace)

    # Deleting construction history
    cmds.delete(ch = True)

    # Assigning material to block
    cmds.hyperShade(assign = (block.namespace + ':blockMat'))

    # Removing block namespace
    cmds.namespace(removeNamespace = ':' + block.namespace, mergeNamespaceWithParent = True)

# Main Code ---------------------------------------------------------------------------

# Creating window

# Making sure there are no windows with duplicate names
if cmds.window(WINDOW_NAME, exists = True):
    cmds.deleteUI(WINDOW_NAME, window = True)

# Setting window dimensions
window = cmds.window(WINDOW_NAME, menuBar = True, resizeToFitChildren = True)

# Creating window menu
cmds.menu(label = 'Basic Options')
cmds.menuItem(label = 'New Scene', command = ('cmds.file(force = True, new = True)'))
cmds.menuItem(label = 'Delete Selected', command = ('cmds.delete()'))

# Creating window items

# Layout: Standard Block
cmds.setParent()
cmds.frameLayout(collapsable = True, label = 'Standard Block', width = 400)

cmds.setParent()
cmds.columnLayout(columnAttach = ('right', 5), rowSpacing = 10, columnWidth = 375)

# Size slider
cmds.intSliderGrp('standardHeight', l = 'Height', f = True, min = 1, max = 16, value = 3)
cmds.intSliderGrp('standardWidth', l = 'Width (Bumps)', f = True, min = 1, max = 16, value = 2)
cmds.intSliderGrp('standardDepth', l = 'Depth (Bumps)', f = True, min = 1, max = 16, value = 8)

# Colour slider
cmds.colorSliderGrp('standardColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l = 'Create Standard Block', command = ('standardBlock()'))

cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# Layout: Tile Block
cmds.setParent()
cmds.frameLayout(collapsable = True, label = 'Tile Block', width = 400)

cmds.setParent()
cmds.columnLayout(columnAttach = ('right', 5), rowSpacing = 10, columnWidth = 375)

# Size slider
cmds.intSliderGrp('tileWidth', l = 'Width', f = True, min = 1, max = 16, value = 2)
cmds.intSliderGrp('tileDepth', l = 'Depth', f = True, min = 1, max = 16, value = 8)

# Colour slider
cmds.colorSliderGrp('tileColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l = 'Create Tile Block', command = ('tileBlock()'))

cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# Layout: Jumper Block
cmds.setParent()
cmds.frameLayout(collapsable = True, label = 'Jumper Block', width = 400)

cmds.setParent()
cmds.columnLayout(columnAttach = ('right', 5), rowSpacing = 10, columnWidth = 375)

# Size slider
cmds.intSliderGrp('jumperHeight', l = 'Height', f = True, min = 1, max = 16, value = 1)
cmds.intSliderGrp('jumperWidth', l = 'Width (Bumps)', f = True, min = 1, max = 16, value = 2)
cmds.intSliderGrp('jumperDepth', l = 'Depth (Bumps)', f = True, min = 1, max = 16, value = 1)

# Colour slider
cmds.colorSliderGrp('jumperColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l = 'Create Jumper Block', command = ('jumperBlock()'))

cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# Layout: 4 Sided Block
cmds.setParent()
cmds.frameLayout(collapsable = True, label = '4 Sided Block', width = 400)

cmds.setParent()
cmds.columnLayout(columnAttach = ('right', 5), rowSpacing = 10, columnWidth = 375)

# Size slider
cmds.intSliderGrp('fourSideHeight', l = 'Height (Bumps)', f = True, min = 1, max = 16, value = 1)
cmds.intSliderGrp('fourSideWidth', l = 'Width (Bumps)', f = True, min = 1, max = 16, value = 1)
cmds.intSliderGrp('fourSideDepth', l = 'Depth (Bumps)', f = True, min = 1, max = 16, value = 1)

# Colour slider
cmds.colorSliderGrp('fourSideColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l = 'Create 4 Sided Block', command = ('fourSideBlock()'))

cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# Layout: Round Block
cmds.setParent()
cmds.frameLayout(collapsable = True, label = 'Round Block', width = 400)

cmds.setParent()
cmds.columnLayout(columnAttach = ('right', 5), rowSpacing = 10, columnWidth = 375)

# Colour slider
cmds.colorSliderGrp('roundColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l = 'Create Round Block', command = ('roundBlock()'))

cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# Layout: Thin Jumper Block
cmds.setParent()
cmds.frameLayout(collapsable = True, label = 'Thin Jumper Block', width = 400)

cmds.setParent()
cmds.columnLayout(columnAttach = ('right', 5), rowSpacing = 10, columnWidth = 375)

# Size slider
cmds.intSliderGrp('thinJumperHeight', l = 'Height', f = True, min = 1, max = 16, value = 1)
cmds.intSliderGrp('thinJumperWidth', l = 'Width (Bumps)', f = True, min = 1, max = 16, value = 2)

# Colour slider
cmds.colorSliderGrp('thinJumperColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l = 'Create Thin Jumper Block', command = ('thinJumperBlock()'))

cmds.setParent("..")
cmds.setParent("..")

# Layout: Corner Block
cmds.setParent()
cmds.frameLayout(collapsable = True, label = 'Corner Block', width = 400)

cmds.setParent()
cmds.columnLayout(columnAttach = ('right', 5), rowSpacing = 10, columnWidth = 375)

# Size slider
cmds.intSliderGrp('cornerHeight', l = 'Height', f = True, min = 1, max = 16, value = 1)

# Colour slider
cmds.colorSliderGrp('cornerColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l = 'Create Corner Block', command = ('cornerBlock()'))

cmds.setParent("..")

# Layout: Shelf Block
cmds.setParent()
cmds.frameLayout(collapsable=True, label='Shelf Block', width=400)

cmds.setParent()
cmds.columnLayout(columnAttach=('right', 5), rowSpacing=10, columnWidth=375)

# Colour slider
cmds.colorSliderGrp('shelfColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button
cmds.button(l='Create Shelf Block', command=('shelfBlock()'))

cmds.setParent("..")
cmds.setParent("..")
cmds.setParent("..")

# Layout: Four Bump Block
cmds.setParent()  # Go back to the main column layout if needed
cmds.frameLayout(collapsable=True, label='Four Bump Block', width=400)

cmds.setParent()  # Adjust if necessary
cmds.columnLayout(columnAttach=('right', 5), rowSpacing=10, columnWidth=375)

# Colour slider for Four Bump Block
cmds.colorSliderGrp('fourBumpColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button for Four Bump Block
cmds.button(label='Create Four Bump Block', command=('fourBumpBlock()'))

#Layout: Six Bump Block
cmds.setParent()
cmds.frameLayout(collapsable=True, label='Six Bump Block', width=400)

cmds.setParent()
cmds.columnLayout(columnAttach=('right', 5), rowSpacing=10, columnWidth=375)

# Size sliders for sixBumpBlock
#cmds.intSliderGrp('sixBumpWidth', label='Width', field=True, minValue=1, maxValue=10, value=2)
#cmds.intSliderGrp('sixBumpHeight', label='Height', field=True, minValue=1, maxValue=10, value=3)  # Adjust for extra height
#cmds.intSliderGrp('sixBumpDepth', label='Depth', field=True, minValue=1, maxValue=10, value=1)

# Colour slider for sixBumpBlock
cmds.colorSliderGrp('sixBumpColour', l = 'Colour', hsv = (0, 0, 1))

cmds.setParent()

# Create button for sixBumpBlock
cmds.button(label='Create Six Bump Block', command=('sixBumpBlock()'))

cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')
    
# Showing window
cmds.showWindow(window)