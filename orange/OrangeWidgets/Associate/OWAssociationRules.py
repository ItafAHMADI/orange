"""
<name>Association Rules</name>
<description>Association rules inducer</description>
<category>Associations</category>
<icon>icons/AssociationRules.png</icon>
<priority>100</priority>
"""

import orange
from OData import *
from OWWidget import *
import orngAssoc, OWGUI

class OWAssociationRules(OWWidget):
    def __init__(self,parent=None):
        OWWidget.__init__(self,
            parent,
            "AssociationRules",
            "OWAssociationRules is orange widget\n for building Association rules.\n\nAuthors: J. Germovsek, P. Kralj, M. Jursic, J. Demsar",
            FALSE,
            FALSE,
            "OrangeWidgetsIcon.png",
            "OrangeWidgetsLogo.png")

        self.inputs = [("Examples", ExampleTable, self.cdata, 1)]
        self.outputs = [("Association Rules", orange.AssociationRules),("Classifier", orange.Classifier),("Naive Bayesian Classifier", orange.BayesClassifier)]

        self.settingsList = ["useSparseAlgorithm", "classificationRules", "minSupport", "minConfidence", "maxRules"]
        self.loadSettings()
                
        self.dataset = None

        self.useSparseAlgorithm = 0
        self.classificationRules = 0
        box = OWGUI.widgetBox(self.space, "Build algorithm")
        self.cbSparseAlgorithm = OWGUI.checkBox(box, self, 'useSparseAlgorithm', 'Use algorithm for sparse data', tooltip="Use original Agrawal's algorithm", callback = self.checkSparse)
        self.cbClassificationRules = OWGUI.checkBox(box, self, 'classificationRules', 'Induce classification rules', tooltip="Induce classifaction rules")

        self.minSupport = 20
        self.minConfidence = 20
        self.maxRules = 10000
        OWGUI.hSlider(self.space, self, 'minSupport', box='Minimal support [%]', minValue=10, maxValue=100, ticks=10, step = 1)
        OWGUI.hSlider(self.space, self, 'minConfidence', box='Minimal confidence [%]', minValue=10, maxValue=100, ticks=10, step = 1)
        OWGUI.hSlider(self.space, self, 'maxRules', box='Maximal number of rules', minValue=10000, maxValue=100000, step=10000, ticks=10000)

        # Generate button
        self.btnGenerate = QPushButton("&Build rules", self.space)
        self.connect(self.btnGenerate,SIGNAL("clicked()"), self.generateRules)

        self.resize(150,100)


    def generateRules(self):
        if self.dataset:
            num_steps = 20
            for i in range(num_steps):
                build_support = 1 - float(i) / num_steps * (1 - self.minSupport/100.0)
                if self.useSparseAlgorithm:
                    rules = orange.AssociationRulesSparseInducer(self.dataset, support = build_support, confidence = self.minConfidence/100.)
                else:
                    rules = orange.AssociationRulesInducer(self.dataset, support = build_support, confidence = self.minConfidence/100., classificationRules = self.classificationRules)
                if len(rules) >= self.maxRules:
                    break
            self.send("Association Rules", rules)

    def checkSparse(self):
        state = self.cbSparseAlgorithm.isChecked()
        if state:
            self.cbClassificationRules.setEnabled(0)
            self.cbClassificationRules.setChecked(0)
        else:
            self.cbClassificationRules.setEnabled(1)
        
    def cdata(self,dataset):
        self.dataset = dataset
        self.generateRules()

if __name__=="__main__":
    a=QApplication(sys.argv)
    ow=OWAssociationRules()
    a.setMainWidget(ow)

    data = orange.ExampleTable("car")
    ow.cdata(data)
    
    ow.show()
    a.exec_loop()
    ow.saveSettings()
    