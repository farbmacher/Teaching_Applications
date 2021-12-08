import pandas as pd
import numpy as np

def prepare_data():
    """
    Reads the original dataset from AK91 (QOB_tableV.dta) and creates
    all necessary dummy variables (also interaction terms)
    Output is a DataFrame with 329'509 observations and 1597 variables.
    """
    url = "https://raw.githubusercontent.com/farbmacher/Teaching_Applications/main/datasets/AK91/QOB_tableV.dta"

    AK91 = pd.read_stata(url).loc[:, ["LWKLYWGE", "EDUC", "QOB", "YOB", "v22"]].rename(columns={"LWKLYWGE": "logwage", "EDUC": "educ", "v22": "POB"})

    # create dummies from categorical variables
    POBdummies = pd.get_dummies(AK91["POB"], prefix="POB")
    AK91[POBdummies.columns] = POBdummies
    YOBdummies = pd.get_dummies(AK91["YOB"], prefix="YOB")
    AK91[YOBdummies.columns] = YOBdummies
    QOBdummies = pd.get_dummies(AK91["QOB"], prefix="QOB")
    AK91[QOBdummies.columns] = QOBdummies

    # create interactions ob the 3 QOB with 50 POB and 9 YOB dummies
    for qob in list(QOBdummies.columns)[:3]:
        for pob in list(POBdummies.columns)[1:]:
            AK91["QP_{}".format(str(qob[4:])+str(pob[4:]))] = AK91["QOB_{}".format(qob[4:])] * AK91["POB_{}".format(pob[4:])]
    for qob in list(QOBdummies.columns)[:3]:
        for yob in list(YOBdummies.columns)[1:]:
            AK91["QY_{}".format(str(qob[4:])+str(yob[4:]))] = AK91["QOB_{}".format(qob[4:])] * AK91["YOB_{}".format(yob[4:])]
    for qob in list(QOBdummies.columns)[:3]:
        for yob in list(YOBdummies.columns)[1:]:
            for pob in list(POBdummies.columns)[1:]:
                AK91["QYP_{i1}_{i2}_{i3}".format(i1=str(qob[4:]), i2=str(yob[4:]), i3=str(pob[4:]))] = AK91[qob] * AK91[yob]  * AK91[pob]

    # drop categorical variables
    #AK91 = AK91.drop(columns=["QOB", "YOB", "POB",])
    # convert dummy variables from datatype int to bool
    AK91 = AK91.astype(dict.fromkeys(AK91.columns[5:], bool))

    #print("QOB, YOB, POB, QOB+QOB*YOB+QOB*POB, QOB+QOB*YOB+QOB*POB+QOB*YOB*POB")
    len(QOB), len(YOB), len(POB), len(QOB)+len(QOB)*len(YOB)+len(QOB)*len(POB), len(IQYP)+len(IQP)+len(IQY)+len(QOB)
    return AK91

def get_dummy_names(ak91):
    """
    returns a tupel containing 6 lists of variable names
    corresponding to all dummy variables for 
    (QOB, YOB, POB, IQP, IQY, IQYP), facilitating access 
    to certain groups of dummy variables e.g. all quarter of birth dummies
    """
    
    QOB = list(ak91.columns)[66:69]
    YOB = list(ak91.columns)[57:66]
    POB = list(ak91.columns)[6:56]

    IQP = list(ak91.columns)[70:220]
    IQY = list(ak91.columns)[220:247]
    IQYP= list(ak91.columns)[247:]
    return (QOB, YOB, POB, IQP, IQY, IQYP)
