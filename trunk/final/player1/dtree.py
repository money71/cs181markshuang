#!/usr/bin/env python

"""
dtree.py

Implements decision trees, decision stumps, decision tree pruning, and
adaptive boosting, copied from CS181 homework
"""


import math


def log2(dbl):
    return math.log(dbl)/math.log(2.0) if dbl > 0.0 else 0.0


class Instance(object):
    """Describes a piece of data. The features are contained in listAttrs,
    the instance label in fLabel, and the instance weight (for use in boosting)
    in dblWeight.
    """
    def __init__(self, listAttrs, fLabel=None, dblWeight=1.0):
        self.listAttrs = listAttrs
        self.fLabel = fLabel
        self.dblWeight = dblWeight
    def copy(self):
        return Instance(list(self.listAttrs), self.fLabel, self.dblWeight)
    def __repr__(self):
        """This function is called when you 'print' an instance."""
        if self.dblWeight == 1.0:
            return "Instance(%r, %r)" % (self.listAttrs, self.fLabel)
        return ("Instance(%r, %r, %.2f)"
                % (self.listAttrs, self.fLabel, self.dblWeight))


def compute_entropy(dblWeightTrue,dblWeightFalse):
    """ Given the total weight of true instances and the total weight
    of false instances in a collection, return the entropy of this
    collection.
    >>> compute_entropy(0.0,1000.0)
    -0.0
    >>> compute_entropy(0.0001, 0.0)
    -0.0
    >>> compute_entropy(10.0,10.0)
    1.0
    """
    t = dblWeightTrue / (dblWeightTrue + dblWeightFalse)
    f = dblWeightFalse / (dblWeightTrue + dblWeightFalse)
    return -t*log2(t) - f*log2(f)


def separate_by_attribute(listInst, ixAttr):
    """Build a dictionary mapping attribute values to lists of instances.
    
    >>> separate_by_attribute([Instance([5,0],True),Instance([9,0],True)], 0)
    {9: [Instance([9, 0], True)], 5: [Instance([5, 0], True)]}
    """
    d = {}
    for inst in listInst:
        attrVal = inst.listAttrs[ixAttr]
        d.setdefault(attrVal, []).append(inst)
    return d


def compute_entropy_of_split(dictInst):
    """Compute the average entropy of a mapping of attribute values to lists
    of instances.
    The average should be weighted by the sum of the weight in each list of
    instances.
    >>> listInst0 = [Instance([],True,0.5), Instance([],False,0.5)]
    >>> listInst1 = [Instance([],False,3.0), Instance([],True,0.0)]
    >>> dictInst = {0: listInst0, 1: listInst1}
    >>> compute_entropy_of_split(dictInst)
    0.25
    """
    wtotal = 0
    etotal = 0
    for k, v in dictInst.iteritems():
        wt = sum([inst.dblWeight for inst in v if inst.fLabel])
        wf = sum([inst.dblWeight for inst in v if not inst.fLabel])
        w = wt + wf
        etotal += w * compute_entropy(wt, wf)
        wtotal += w
    return etotal / wtotal


def compute_list_entropy(listInst):
    return compute_entropy_of_split({None:listInst})


def choose_split_attribute(iterableIxAttr, listInst, dblMinGain=0.0):
    """Given an iterator over attributes, choose the attribute which
    maximimizes the information gain of separating a collection of
    instances based on that attribute.
    Returns a tuple of (the integer best attribute, a dictionary of the
    separated instances).
    If the best information gain is less than dblMinGain, then return the
    pair (None,None).

    >>> listInst = [Instance([0,0],False), Instance([0,1],True)]
    >>> choose_split_attribute([0,1], listInst)
    (1, {0: [Instance([0, 0], False)], 1: [Instance([0, 1], True)]})
    """
    bestattr = None
    bestgain = dblMinGain
    etotal = compute_list_entropy(listInst)
    for attr in iterableIxAttr:
        e = compute_entropy_of_split(separate_by_attribute(listInst, attr))
        gain = etotal - e
        if gain >= bestgain:
            bestattr = attr
            bestgain = gain
    if bestattr is None:
        return None, None
    return bestattr, separate_by_attribute(listInst,bestattr)


def check_for_common_label(listInst):
    """Return the boolean label shared by all instances in the given list of
    instances, or None if no such label exists.

    >>> check_for_common_label([Instance([],True), Instance([],True)])
    True
    >>> check_for_common_label([Instance([],False), Instance([],False)])
    False
    >>> check_for_common_label([Instance([],True), Instance([],False)])
    """
    val = None
    for inst in listInst:
        if val is None:
            val = inst.fLabel
        if val != inst.fLabel:
            return None
    return val


def majority_label(listInst):
    """Return the boolean label with the most weight in the given list of
    instances.
    
    >>> majority_label([Instance([],True,1.0),Instance([],False,0.75)])
    True
    >>> listInst =[Instance([],False),Instance([],True),Instance([],False)]
    >>> majority_label(listInst)
    False
    """
    tw = 0
    fw = 0
    for inst in listInst:
        if inst.fLabel:
            tw += inst.dblWeight
        else:
            fw += inst.dblWeight
    return tw > fw


class DTree(object):
    def __init__(self, fLabel=None, ixAttr=None, fDefaultLabel=None):
        if fLabel is None and ixAttr is None:
            raise TypeError("DTree must be given a label or an attribute,"
                            " but received neither.")
        self.fLabel = fLabel
        self.ixAttr = ixAttr
        self.dictChildren = {}
        self.fDefaultLabel = fDefaultLabel
        if self.is_node() and self.fDefaultLabel is None:
            raise TypeError("Nodes require a valid fDefaultLabel")
    def is_leaf(self):
        return self.fLabel is not None
    def is_node(self):
        return self.ixAttr is not None
    def add(self, dtChild, v):
        if not isinstance(dtChild,self.__class__):
            raise TypeError("dtChild was not a DTree")
        if v in self.dictChildren:
            raise ValueError("Attempted to add a child with"
                             " an existing attribute value.")
        self.dictChildren[v] = dtChild
    def convert_to_leaf(self):
        if self.is_leaf():
            return
        self.fLabel = self.fDefaultLabel
        self.ixAttr = None
        self.fDefaultLabel = None
        self.dictChildren = {}
    # the following methods are used in testing -- you should need
    # to worry about them
    def copy(self):
        if self.is_leaf():
            return DTree(fLabel=self.fLabel)
        dt = DTree(ixAttr=self.ixAttr, fDefaultLabel=self.fDefaultLabel)
        for ixValue,dtChild in self.dictChildren.iteritems():
            dt.add(dtChild.copy(),ixValue)
        return dt
    def _append_repr(self,listRepr):
        if self.is_leaf():
            listRepr.append("[%s]" % str(self.fLabel)[0])
        else:
            sDefaultLabel = str(self.fDefaultLabel)[0]
            listRepr.append("<%d,%s,{" % (self.ixAttr, sDefaultLabel))
            for dtChild in self.dictChildren.values():
                dtChild._append_repr(listRepr)
            listRepr.append("}>")
    def __repr__(self):
        listRepr = []
        self._append_repr(listRepr)
        return "".join(listRepr)


def build_tree_rec(setIxAttr, listInst, dblMinGain, cRemainingLevels):
    """Recursively build a decision tree.

    Given a set of integer attributes, a list of instances, a boolean default
    label, and a floating-point valued minimum information gain, create
    a decision tree leaf or node.

    If there is a common label across all instances in listInst, the function
    returns a leaf node with this common label.

    If setIxAttr is empty, the function returns a leaf with the majority label
    across listInst.

    If cRemainingLevels is zero, return the majority label. (If
    cRemainingLevels is less than zero, then we don't want to do anything
    special -- this is our mechanism for ignoring the tree depth limit).

    If no separation of the instances yields an information gain greater than
    dblMinGain, the function returns a leaf with the majority label across
    listInst.

    Otherwise, the function finds the attribute which maximizes information
    gain, splits on the attribute, and continues building the tree
    recursively.

    When building tree nodes, the function specifies the majority label across
    listInst as the node's default label (fDefaultLabel argument to DTree's
    __init__). This will be useful in pruning.
    """
    label = check_for_common_label(listInst)
    if label is not None:
        return DTree(fLabel = label)
    if not setIxAttr:
        return DTree(fLabel = majority_label(listInst))
    if cRemainingLevels == 0:
        return DTree(fLabel = majority_label(listInst))
    attr, newdict = choose_split_attribute(setIxAttr, listInst, dblMinGain)
    if attr is None:
        return DTree(fLabel = majority_label(listInst))
    d = DTree(ixAttr = attr, fDefaultLabel = majority_label(listInst))
    setIxPrime = set(setIxAttr) - set([attr])
    for k,v in newdict.iteritems():
        d.add(build_tree_rec(setIxPrime,v,dblMinGain, cRemainingLevels-1), k)
    return d


def count_instance_attributes(listInst):
    """Return the number of attributes across all instances, or None if the
    instances differ in the number of attributes they contain.

    >>> listInst = [Instance([1,2,3],True), Instance([4,5,6],False)]
    >>> count_instance_attributes(listInst)
    3
    >>> count_instance_attributes([Instance([1,2],True),Instance([3],False)])
    """
    i = None
    for inst in listInst:
        if i is None:
            i = len(inst.listAttrs)
        elif i != len(inst.listAttrs):
            return None
    return i


def build_tree(listInst, dblMinGain=0.0, cMaxLevel=-1):
    """Build a decision tree with the ID3 algorithm from a list of
    instances.
    """
    cAttr = count_instance_attributes(listInst)
    if cAttr is None:
        raise TypeError("Instances provided have attribute lists of "
                        "varying lengths.")
    setIxAttr = set(xrange(cAttr))
    return build_tree_rec(setIxAttr, listInst, dblMinGain, cMaxLevel)


def classify(dt, inst):
    """Using decision tree dt, return the label for instance inst."""
    if dt.is_leaf():
        return dt.fLabel
    elif inst.listAttrs[dt.ixAttr] in dt.dictChildren:
        return classify(dt.dictChildren[inst.listAttrs[dt.ixAttr]], inst)
    return dt.fDefaultLabel


class EvaluationResult(object):
    def __init__(self, listInstCorrect, listInstIncorrect, oClassifier):
        self.listInstCorrect = listInstCorrect
        self.listInstIncorrect = listInstIncorrect
        self.oClassifier = oClassifier


def weight_correct_incorrect(rslt):
    """Return a pair of floating-point numbers denoting the weight of
    (correct, incorrect) instances in EvaluationResult rslt.

    >>> listInstCorrect = [Instance([],True,0.25)]
    >>> listInstIncorrect = [Instance([],False,0.50)]
    >>> rslt = EvaluationResult(listInstCorrect, listInstIncorrect, None)
    >>> weight_correct_incorrect(rslt)
    (0.25, 0.5)
    """
    c = 0
    i = 0
    for inst in rslt.listInstCorrect:
        c += inst.dblWeight
    for inst in rslt.listInstIncorrect:
        i += inst.dblWeight
    return c, i


class CrossValidationFold(object):
    def build(self):
        raise NotImplemented
    def classify(self, dt, inst):
        raise NotImplemented
    def check_insts(self, listInst):
        for inst in (listInst or []):
            if inst.fLabel is None:
                raise TypeError("missing instance label")
        return listInst


class TreeFold(CrossValidationFold):
    def __init__(self, listInstTraining, listInstTest, listInstValidate=None):
        super(TreeFold,self).__init__()
        self.listInstTraining = self.check_insts(listInstTraining)
        self.listInstTest = self.check_insts(listInstTest)
        self.listInstValidate = self.check_insts(listInstValidate)
        self.cMaxLevel = -1
    def build(self):
        return build_tree(self.listInstTraining, cMaxLevel=self.cMaxLevel)
    def classify(self, dt, inst):
        return classify(dt,inst)


def evaluate_classification(cvf):
    """Given a CrossValidationFold, build a classifier and build an
    EvaluationResult that correctly partitions test instances into a list of
    correctly and incorrectly classified instances.

    Classifiers can be built using cvf.build().

    Evaluation results are built with
    EvaluationResult(listInstCorrect,listInstIncorrect,dt)
    where dt is the classifier built with cvf.build().
    """
    lc = []
    li = []
    dt = cvf.build()
    for inst in cvf.listInstTest:
        if cvf.classify(dt,inst) == inst.fLabel:
            lc.append(inst)
        else:
            li.append(inst)
    evalRslt = EvaluationResult(lc,li,dt)
    return evalRslt


def check_folds(listInst, cFold, cMinFold):
    """Raise a ValueError if cFold is greater than the number of instances, or
    if cFold is less than the minimum number of folds.

    >>> check_folds([Instance([],True), Instance([],False)], 1, 2)
    >>> check_folds([Instance([],True)], 2, 1)
    Traceback (most recent call last):
    ...
    ValueError: Cannot have more folds than instances
    >>> check_folds([Instance([],False)], 1, 2)
    Traceback (most recent call last):
    ...
    ValueError: Need at least 2 folds.
    """
    if cFold > len(listInst):
        raise ValueError('Cannot have more folds than instances')
    if cFold < cMinFold:
        raise ValueError('Need at least %d folds' % (cMinFold))
    return


def yield_cv_folds(listInst, cFold):
    """Yield a series of TreeFolds, which represent a partition of listInst
    into cFold folds.

    You may either return a list, or `yield` (http://goo.gl/gwOfM)
    TreeFolds one at a time.
    """
    check_folds(listInst, cFold, 2)
    n = len(listInst)
    foldsize = int(math.ceil(n / cFold))
    ret = []
    for i in xrange(cFold):
        ind1 = i * foldsize
        ind2 = (i+1) * foldsize
        test = listInst[ind1:ind2]
        training = listInst[:ind1]
        training.extend(listInst[ind2:])
        ret.append(TreeFold(training, test))
    return ret


def cv_score(iterableFolds):
    """Determine the fraction (by weight) of correct instances across a number
    of cross-validation folds.
    """
    c = 0.0
    i = 0.0
    for fold in iterableFolds:
        cp, ip = weight_correct_incorrect(evaluate_classification(fold))
        c += cp
        i += ip
    return c/(c+i)


def prune_tree(dt, listInst):
    """Recursively prune a decision tree.

    Given a subtree to prune and a list of instances,
    recursively prune the tree, then determine if the current node should
    become a leaf.

    The function does not return anything, and instead modifies the tree
    in-place.
    """
    score = 0
    scorePruned = 0
    if dt.is_leaf():
        return
    dictInst = separate_by_attribute(listInst,dt.ixAttr)
    for v, listInstChild in dictInst.iteritems():
        if v in dt.dictChildren:
            prune_tree(dt.dictChildren[v],listInstChild)
    for inst in listInst:
        if classify(dt,inst) == inst.fLabel:
            score += inst.dblWeight
        if dt.fDefaultLabel == inst.fLabel:
            scorePruned += inst.dblWeight
    if scorePruned >= score:
        dt.convert_to_leaf()


def build_pruned_tree(listInstTrain, listInstValidate):
    """Build a pruned decision tree from a list of training instances, then
    prune the tree using a list of validation instances.

    Return the pruned decision tree.
    """
    dt = build_tree(listInstTrain)
    prune_tree(dt, listInstValidate)
    return dt


class PrunedFold(TreeFold):
    def __init__(self, *args, **kwargs):
        super(PrunedFold,self).__init__(*args,**kwargs)
        if self.listInstValidate is None:
            raise TypeError("PrunedCrossValidationFold requires "
                            "listInstValidate argument.")
    def build(self):
        return build_pruned_tree(self.listInstTraining,self.listInstValidate)


def yield_cv_folds_with_validation(listInst, cFold):
    """Yield a number cFold of PrunedFolds, which together form a partition of
    the list of instances listInst.

    You may either return a list or yield successive values.
    """
    check_folds(listInst, cFold, 3)
    n = len(listInst)
    foldsize = int(math.ceil(n / cFold))
    ret = []
    for i in xrange(cFold):
        ind1 = i * foldsize
        ind2 = (i+1) * foldsize
        test = listInst[ind1:ind2]
        if ind2 == n:
            validate = listInst[:foldsize]
            training = listInst[foldsize:ind1]
        else:
            ind3 = min(n, ind2+foldsize)
            validate = listInst[ind2:ind3]
            training = listInst[:ind1]
            training.extend(listInst[ind3:])
        ret.append(PrunedFold(training, test, validate))
    return ret


def normalize_weights(listInst):
    """Normalize the weights of all the instances in listInst so that the sum
    of their weights totals to 1.0.
    
    The function modifies the weights of the instances in-place and does
    not return anything.

    >>> listInst = [Instance([],True,0.1), Instance([],False,0.3)]
    >>> normalize_weights(listInst)
    >>> print listInst
    [Instance([], True, 0.25), Instance([], False, 0.75)]
    """
    t = 0
    for i in listInst:
        t += i.dblWeight
    for i in listInst:
        i.dblWeight = i.dblWeight/t


def init_weights(listInst):
    """Initialize the weights of the instances in listInst so that each
    instance has weight 1/(number of instances). This function modifies
    the weights in place and does not return anything.

    >>> listInst = [Instance([],True,0.5), Instance([],True,0.25)]
    >>> init_weights(listInst)
    >>> print listInst
    [Instance([], True, 0.50), Instance([], True, 0.50)]
    """
    for i in listInst:
        i.dblWeight = 1.0
    normalize_weights(listInst)


def classifier_error(rslt):
    """Given and evaluation result, return the (floating-point) fraction
    of correct instances by weight.

    >>> listInstCorrect = [Instance([],True,0.15)]
    >>> listInstIncorrect = [Instance([],True,0.45)]
    >>> rslt = EvaluationResult(listInstCorrect,listInstIncorrect,None)
    >>> classifier_error(rslt)
    0.75
    """
    c, i = weight_correct_incorrect(rslt)
    return i / (c+i)


def classifier_weight(dblError):
    """Return the classifier weight alpha from the classifier's training
    error.
    """
    return 0.5 * math.log((1.0-dblError) / dblError)


def update_weight_unnormalized(inst, dblClassifierWeight, fClassifiedLabel):
    """Re-weight an instance given the classifier weight, and the label
    assigned to the instance by the classifier. This function acts in place
    and does not return anything.
    """
    if inst.fLabel == fClassifiedLabel:
        inst.dblWeight = inst.dblWeight * math.exp(-dblClassifierWeight)
    else:
        inst.dblWeight = inst.dblWeight * math.exp(dblClassifierWeight)


class StumpFold(TreeFold):
    def __init__(self, listInstTraining, cMaxLevel=1):
        self.listInstTraining = listInstTraining
        self.listInstTest = listInstTraining
        self.cMaxLevel = cMaxLevel
    def build(self):
        return build_tree(self.listInstTraining, cMaxLevel=self.cMaxLevel)


def one_round_boost(listInst, cMaxLevel):
    """Conduct a single round of boosting on a list of instances. Returns a
    triple (classifier, error, classifier weight).

    Implementation suggestion:
    - build a StumpFold from the list of instances and the given
      cMaxLevel (it's obnoxious that cMaxLevel has to be passed around
      like this -- just pass it into Stumpfold() as the second argument
      and you should be fine).
    - using the StumpFold, build an EvaluationResult using
      evaluate_classification
    - get the error rate of the EvaluationResult using classifier_error
    - obtain the classifier weight from the classifier error
    - update the weight of all instances in the evaluation results
    - normalize all weights
    - return the EvaluationResult's oClassifier member, the classifier error,
      and the classifier weight in a 3-tuple
    - remember to return early if the error is zero.
    """
    sf = StumpFold(listInst, cMaxLevel)
    eRslt = evaluate_classification(sf)
    e = classifier_error(eRslt)
    if e == 0:
        return eRslt.oClassifier, 0, 1
    w = classifier_weight(e)
    for inst in eRslt.listInstCorrect:
        update_weight_unnormalized(inst, w, inst.fLabel)
    for inst in eRslt.listInstIncorrect:
        update_weight_unnormalized(inst, w, not inst.fLabel)
    normalize_weights(listInst)
    return eRslt.oClassifier, e, w


class BoostResult(object):
    def __init__(self, listDblCferWeight, listCfer):
        self.listDblCferWeight = listDblCferWeight
        self.listCfer = listCfer


def boost(listInst, cMaxRounds=50, cMaxLevel=1):
    """Conduct up to cMaxRounds of boosting on training instances listInst
    and return a BoostResult containing the classifiers and their weights.
    """
    init_weights(listInst)
    lw = []
    lc = []
    for k in xrange(cMaxRounds):
        c, e, w = one_round_boost(listInst, cMaxLevel)
        if e == 0:
            lc = [c]
            lw = [w]
            break
        else:
            lc.append(c)
            lw.append(w)
    return BoostResult(lw, lc)


def classify_boosted(br,inst):
    """Given a BoostResult and an instance, return the (boolean) label
    predicted for the instance by the boosted classifier.
    """
    result = 0
    for dblCferWeight, cfer in zip (br.listDblCferWeight, br.listCfer):
        result += dblCferWeight*(classify(cfer, inst)-0.5)
    return result >= 0


class BoostedFold(TreeFold):
    def __init__(self, *args, **kwargs):
        super(BoostedFold,self).__init__(*args, **kwargs)
        self.cMaxLevel = 1
        self.cMaxRounds = 50        
    def build(self):
        listInst = [inst.copy() for inst in self.listInstTraining]
        return boost(listInst, self.cMaxRounds, self.cMaxLevel)
    def classify(self, br, inst):
        return classify_boosted(br, inst)


def yield_boosted_folds(listInst, cFold):
    """Yield a number cFold of BoostedFolds, constituting a partition of
    listInst.

    Implementation suggestion: Generate TreeFolds, and yield BoostedFolds
    built from your TreeFolds.
    """
    listBf = []
    for tf in yield_cv_folds(listInst, cFold):
        listBf.append(BoostedFold(tf.listInstTraining,tf.listInstTest))
    return listBf
