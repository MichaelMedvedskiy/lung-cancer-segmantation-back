import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from myutils import nms
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


#func defs
def getClean():
    return np.load('./net_results/1_clean.npy')

clean_numpy = getClean()
def getPbb():
    return np.load('./net_results/1_pbb.npy')

#def getPngForSliceNumber(number):


def getClearForSliceNumber(number):
    #check for number > max #
    img = clean_numpy
    output = io.BytesIO()
    #plt.savefig('./test_of_img.png')
    plt.imshow(img[0, number], 'gray')
    ax = plt.subplot(1, 1, 1)
    [p.remove() for p in reversed(ax.patches)]
    modifyReturnBasedOnWhetherSliceNumberIsProposed(ax, number, getPredictionSliceNumbers("TEMPLATE"))
    FigureCanvas(ax.figure).print_png(output)
    print(getPredictionSliceNumbers("TEMPLATE"))
    return output

def modifyReturnBasedOnWhetherSliceNumberIsProposed(ax, current_number, prediction_slice_numbers):
    if current_number in prediction_slice_numbers:
        pbb = getPbb()
        pbb = nms(pbb, 0.05)
        box = pbb[prediction_slice_numbers.index(current_number)].astype('int')[1:]
        rect = patches.Rectangle((box[2]-box[3],box[1]-box[3]),box[3]*2,box[3]*2,linewidth=2,edgecolor='red',facecolor='none')
        ax.add_patch(rect)


def getPredictionSliceNumbers(dicom_id):
    #extract by dicom id
    pbb = getPbb()
    pbb = nms(pbb, 0.05)
    slice_numbers = []
    for pbb_instance in pbb:
        slice_numbers.append(int( pbb_instance.astype('int')[1:][0]))
    return slice_numbers


def getCleanSliceCount():
    clean = clean_numpy
    return int(clean[0].size /clean[0][0].size)

# img = getClean()
# pbb = getPbb()
# pbb = pbb[pbb[:,0]>-1]
#
#
# pbb = nms(pbb,0.05)
# box = pbb[0].astype('int')[1:]
#
# ax = plt.subplot(1,1,1)
# plt.imshow(img[0,0],'gray')
# plt.axis('off')
#
#
# # adding the rectangle of segmentation
# rect = patches.Rectangle((box[2]-box[3],box[1]-box[3]),box[3]*2,box[3]*2,linewidth=2,edgecolor='red',facecolor='none')
# ax.add_patch(rect)
# print(box)
#
#
# output = io.BytesIO()
# FigureCanvas(ax.figure).print_png(output)
# print(output)
# plt.savefig('./test_of_img.png')
#
#
