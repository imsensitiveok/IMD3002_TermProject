import maya.cmds as cmds
import random as rnd

MyWin = 'Lego Blocks'
if cmds.window(MyWin, exists=True):
    cmds.deleteUI(MyWin, window=True)
MyWin = cmds.window(MyWin, menuBar=True, widthHeight=(500,300))

cmds.menu(label="Basic Options")
cmds.menuItem(label="New Scene", command=('cmds.file(new=True,force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

cmds.frameLayout(collapsable=True, label="Standard Block", width=475, height=140)

cmds.columnLayout()

cmds.intSliderGrp('blockHeight', l="Height", f=True, min=1, max=20, value=3)
cmds.intSliderGrp('blockWidth', l="Width (Bumps)", f=True, min=1, max=20, value=2)
cmds.intSliderGrp('blockDepth', l="Depth (Bumps)", f=True, min=1, max=20, value=8)

cmds.colorSliderGrp('blockColour', label="Colour", hsv=(120, 1, 1))

cmds.columnLayout()
cmds.button(label="Create Basic Block", command=('basicBlock()'))
cmds.setParent('..')

cmds.setParent('..')
cmds.setParent('..')

cmds.frameLayout(collapsable=True, label="Sloped Block", width=475, height=160)
cmds.columnLayout()
cmds.intSliderGrp('slopedWidth', l="Width (Bumps)", f=True, min=1, max=20, v=4)
cmds.intSliderGrp('slopedDepth', l="Depth (Bumps)", f=True, min=2, max=4, v=2)
cmds.colorSliderGrp('slopedColour', l="Colour", hsv=(12, 1, 1))

cmds.columnLayout()
cmds.button(label="Create Sloped Block", command=('slopedBlock()'))
cmds.setParent('..')

cmds.setParent('..')
cmds.setParent('..')

cmds.showWindow(MyWin)


def slopedBlock():
    print("Sloped Block")
    blockHeight = 3
    blockWidth = cmds.intSliderGrp('slopedWidth', q=True, v=True)
    blockDepth = cmds.intSliderGrp('slopedDepth', q=True, v=True)
    rgb = cmds.colorSliderGrp('slopedColour', q=True, rgbValue=True)

    nsTmp = "Block" + str(rnd.randint(1000, 9999))
    cmds.select(clear=True)
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)

    cubeSizeX = blockWidth * 0.8
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32

    cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ, sz=blockDepth)
    cmds.move((cubeSizeY / 2.0), y=True, a=True)

    for i in range(blockWidth):
        cmds.polyCylinder(r=0.25, h=0.20)
        cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
        cmds.move(((i * 0.8) - (cubeSizeX / 2.0) + 0.4), moveX=True, a=True)
        cmds.move((0 - (cubeSizeZ / 2.0) + 0.4), moveZ=True)

    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp + ": blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')

    cmds.polyUnite((nsTmp + ":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)

    cmds.hyperShade(assign=(nsTmp + ":blckMat"))

    cmds.select((nsTmp + ":" + nsTmp + ".e[1]"), r=True)
    cmds.move(0, -0.8, 0, r=True)

    if blockDepth == 4:
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[8]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[6]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[9]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[7]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

    if blockDepth >= 3:
        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[6]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[4]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

        tV = cmds.xform((nsTmp + ":" + nsTmp + ".vtx[7]"), q=True, t=True)
        cmds.select((nsTmp + ":" + nsTmp + ".vtx[5]"), r=True)
        cmds.move(tV[0], tV[1], tV[2], a=True)

    cmds.namespace(removeNamespace=":" + nsTmp, mergeNamespaceWithParent=True)


def basicBlock():
    print("Basic Block")
    blockHeight = cmds.intSliderGrp('blockHeight', q=True, v=True)
    blockWidth = cmds.intSliderGrp('blockWidth', q=True, v=True)
    blockDepth = cmds.intSliderGrp('blockDepth', q=True, v=True)

    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
    nsTmp = "Block" + str(rnd.randint(1000, 9999))

    cmds.select(clear=True)
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)

    cubeSizeX = blockWidth * 0.8
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32

    cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    cmds.move((cubeSizeY / 2.0), moveY=True)

    for i in range(blockWidth):
        for j in range(blockDepth):
            cmds.polyCylinder(r=0.25, h=0.20)
            cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX / 2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeSizeZ / 2.0) + 0.4), moveZ=True, a=True)

    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp + ":blckMat.color", rgb[0], rgb[1], rgb[2], typ='double3')

    cmds.polyUnite((nsTmp + ":*"), n=nsTmp, ch=True)
    cmds.delete(ch=True)
    cmds.hyperShade(assign=(nsTmp + ":blckMat"))

    cmds.namespace(removeNamespace=":" + nsTmp, mergeNamespaceWithParent=True)
