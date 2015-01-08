import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import math

#
# T1Mapping
#

class T1Mapping(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "T1Mapping" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# T1MappingWidget
#

class T1MappingWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume1 selector
    #
    self.inputSelector1 = slicer.qMRMLNodeComboBox()
    self.inputSelector1.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector1.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector1.selectNodeUponCreation = True
    self.inputSelector1.addEnabled = False
    self.inputSelector1.removeEnabled = False
    self.inputSelector1.noneEnabled = False
    self.inputSelector1.showHidden = False
    self.inputSelector1.showChildNodeTypes = False
    self.inputSelector1.setMRMLScene( slicer.mrmlScene )
    self.inputSelector1.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume 1: ", self.inputSelector1)

    self.screenshotFlipAngleSliderWidget1 = ctk.ctkSliderWidget()
    self.screenshotFlipAngleSliderWidget1.singleStep = 1.0
    self.screenshotFlipAngleSliderWidget1.minimum = 1.0
    self.screenshotFlipAngleSliderWidget1.maximum = 60.0
    self.screenshotFlipAngleSliderWidget1.value = 1.0
    self.screenshotFlipAngleSliderWidget1.setToolTip("Set Flip Angle for the first volume.")
    parametersFormLayout.addRow("First Volume Flip Angle", self.screenshotFlipAngleSliderWidget1)

    #
    # input volume2 selector
    #
    self.inputSelector2 = slicer.qMRMLNodeComboBox()
    self.inputSelector2.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector2.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector2.selectNodeUponCreation = True
    self.inputSelector2.addEnabled = False
    self.inputSelector2.removeEnabled = False
    self.inputSelector2.noneEnabled = False
    self.inputSelector2.showHidden = False
    self.inputSelector2.showChildNodeTypes = False
    self.inputSelector2.setMRMLScene( slicer.mrmlScene )
    self.inputSelector2.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume 2: ", self.inputSelector2)

    self.screenshotFlipAngleSliderWidget2 = ctk.ctkSliderWidget()
    self.screenshotFlipAngleSliderWidget2.singleStep = 1.0
    self.screenshotFlipAngleSliderWidget2.minimum = 1.0
    self.screenshotFlipAngleSliderWidget2.maximum = 60.0
    self.screenshotFlipAngleSliderWidget2.value = 1.0
    self.screenshotFlipAngleSliderWidget2.setToolTip("Set Flip Angle for the first volume.")
    parametersFormLayout.addRow("Second Volume Flip Angle", self.screenshotFlipAngleSliderWidget2)

    self.screenshotRepetitionTimeSliderWidget = ctk.ctkSliderWidget()
    self.screenshotRepetitionTimeSliderWidget.singleStep = 1.0
    self.screenshotRepetitionTimeSliderWidget.minimum = 1.0
    self.screenshotRepetitionTimeSliderWidget.maximum = 100.0
    self.screenshotRepetitionTimeSliderWidget.value = 1.0
    self.screenshotRepetitionTimeSliderWidget.setToolTip("Set Repetition Time in ms")
    parametersFormLayout.addRow("Repetition Time", self.screenshotRepetitionTimeSliderWidget)

    """
    self.outputVolumeNameWidget = qt.QLineEdit()
    #self.outputVolumeName.show()
    parametersFormLayout.addRow("Output Volume Name", self.outputVolumeNameWidget)
    #le.text
    """
    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.outputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    #self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    #self.enableScreenshotsFlagCheckBox.checked = 0
    #self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    #parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    #self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    #self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = T1MappingLogic()
    #enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    #screenshotScaleFactor = int(self.screenshotScaleFactorSliderWidget.value)
    
    #print("Run the algorithm")
    #inputVolume1 = self.inputSelector1.currentNode()
    #print inputVolume1.GetName()
    
    logic.run(self.inputSelector1.currentNode(), self.screenshotFlipAngleSliderWidget1.value, self.inputSelector2.currentNode(), self.screenshotFlipAngleSliderWidget2.value, self.screenshotRepetitionTimeSliderWidget.value, self.outputSelector.currentNode())

#
# T1MappingLogic
#

class T1MappingLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, self.screenshotScaleFactor, imageData)

  def run(self, inputVolume1, flipAngle1, inputVolume2, flipAngle2, tr, outputVolume):
    """
    Run the actual algorithm
    """

    #print"running the algorithm"

    if not (inputVolume1 and inputVolume2):
      print"FATAL ERROR: inputs are not initialized"
      return

    if not outputVolume:
      print"FATAL ERROR: output volume name is not initialized"
      return

    #print inputVolume1
    array_vol1 = slicer.util.array(inputVolume1.GetName())
    #print array_vol1.shape

    array_vol2 = slicer.util.array(inputVolume2.GetName())

    if array_vol1.shape != array_vol2.shape:
      print "FATAL ERROR: Dimensions of the first and second input volumes are not the same"
      return

    #output_vol = slicer.util.array(outputVolume.GetName())
    #print output_vol
    #print outputVolume

    #reuse the name
    #name = outputVolume.GetName()
    #print "output volume name: ", outputVolumeName
    #nasty hack to reuse outputVolume structure. I basically overwrite the outputVolume node
    print "output volume name: ", outputVolume.GetName()
    outputVolume = slicer.vtkSlicerVolumesLogic.CloneVolume(slicer.mrmlScene, inputVolume1, outputVolume.GetName())
    
    outputVolumeArray = slicer.util.array(outputVolume.GetName())
    #set array to zero
    outputVolumeArray.flat[...]=0
    #print outputVolumeNewArray.shape

    # convert flip angles to radians
    #print flipAngle1, flipAngle2

    alpha1 = math.radians(flipAngle1)
    alpha2 = math.radians(flipAngle2)
    #print alpha1, alpha2
    #print "repetition time: ", tr

    for i,val in enumerate(array_vol1.flat):

        x1 = array_vol1.flat[i] / math.tan(alpha1)
        y1 = array_vol1.flat[i] / math.sin(alpha1)

        x2 = array_vol2.flat[i] / math.tan(alpha2)
        y2 = array_vol2.flat[i] / math.sin(alpha2)

        e1 = (y2 - y1) / (x2 - x1)# this is slope which is equil to E1

        if math.isnan(e1):
            e1 = 0
            t1 = 0
            #print "WARNING: e1 is nan for pixel ", i, " vol1 value: ", array_vol1.flat[i], " vol2 value: ", array_vol2.flat[i]

        elif e1 <= 0:# when e1 is less than zero it causes underfined number error for log, avoid it by setting t1 to zero
            e1 = 1.0
            t1 = 0
            #print "WARNING: e1 is less than zero for pixel ", i, " vol1 value: ", array_vol1.flat[i], " vol2 value: ", array_vol2.flat[i]
        else:
            t1 = -tr/math.log(e1)# this is T1
        
        #print x1, y1, x2, y2, e1, t1
        outputVolumeArray.flat[i] = t1        

        #t1_array.flat[i] = t1

    #self.delayDisplay('Running the aglorithm')
    #self.enableScreenshots = enableScreenshots
    #self.screenshotScaleFactor = screenshotScaleFactor
    #self.takeScreenshot('T1Mapping-Start','Start',-1)

    return True


class T1MappingTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_T1Mapping1()

  def test_T1Mapping1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = T1MappingLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
